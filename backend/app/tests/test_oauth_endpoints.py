import re

from httpx import AsyncClient

from app.core.domain.user import OAuthProvider
from app.core.exceptions.oauth import (
    OAuthError,
    OAuthProviderError,
    OAuthTokenExchangeError,
)
from app.core.repositories.oauth_provider import OAuthUserInfo
from app.infrastructure.oauth import GoogleOAuthProvider

from .base import BaseTest


class TestGoogleAuthorizeEndpoint(BaseTest):
    """Tests for the Google OAuth authorization endpoint"""

    async def test_returns_authorization_url_and_state(self, client: AsyncClient):
        """Test that endpoint returns valid authorization URL and state token"""
        response = await client.get("/auth/oauth/google/authorize")

        assert response.status_code == 200
        data = response.json()

        # Validate response structure
        assert "authorization_url" in data
        assert "state" in data

        # Validate state token format (should be URL-safe base64 string)
        state = data["state"]
        assert isinstance(state, str)
        assert len(state) > 0
        # URL-safe base64 tokens should only contain alphanumeric, -, and _
        assert re.match(r"^[A-Za-z0-9_-]+$", state)

        # Validate authorization URL format
        auth_url = data["authorization_url"]
        assert auth_url.startswith("https://accounts.google.com/o/oauth2/v2/auth")
        assert "client_id=" in auth_url
        assert "redirect_uri=" in auth_url
        assert "response_type=code" in auth_url
        assert "scope=openid" in auth_url
        assert f"state={state}" in auth_url

    async def test_sets_oauth_state_cookie(self, client: AsyncClient):
        """Test that endpoint sets oauth_state cookie with correct attributes"""
        response = await client.get("/auth/oauth/google/authorize")

        assert response.status_code == 200
        assert "oauth_state" in response.cookies

        # Validate cookie value matches state in response
        data = response.json()
        assert response.cookies["oauth_state"] == data["state"]

        # Validate cookie attributes via Set-Cookie header
        set_cookie_header = response.headers.get("set-cookie", "")
        assert "oauth_state=" in set_cookie_header
        assert "HttpOnly" in set_cookie_header
        assert "SameSite=none" in set_cookie_header or "samesite=none" in set_cookie_header.lower()
        assert "Max-Age=600" in set_cookie_header

    async def test_state_token_is_unique_per_request(self, client: AsyncClient):
        """Test that each request generates a unique state token"""
        response1 = await client.get("/auth/oauth/google/authorize")
        response2 = await client.get("/auth/oauth/google/authorize")

        assert response1.status_code == 200
        assert response2.status_code == 200

        state1 = response1.json()["state"]
        state2 = response2.json()["state"]

        # State tokens should be different
        assert state1 != state2

        # Cookie values should also be different
        assert response1.cookies["oauth_state"] != response2.cookies["oauth_state"]

    async def test_authorization_url_contains_required_parameters(self, client: AsyncClient):
        """Test that authorization URL contains all required OAuth parameters"""
        response = await client.get("/auth/oauth/google/authorize")

        assert response.status_code == 200
        auth_url = response.json()["authorization_url"]

        # Parse query parameters from URL
        assert "response_type=code" in auth_url
        assert "scope=" in auth_url
        assert "access_type=offline" in auth_url
        assert "prompt=consent" in auth_url

    async def test_response_matches_schema(self, client: AsyncClient):
        """Test that response matches OAuthAuthorizeResponse schema"""
        response = await client.get("/auth/oauth/google/authorize")

        assert response.status_code == 200
        data = response.json()

        # Validate response has required fields
        assert "authorization_url" in data
        assert "state" in data
        assert isinstance(data["authorization_url"], str)
        assert isinstance(data["state"], str)
        assert len(data["state"]) > 0

    async def test_cookie_expires_in_10_minutes(self, client: AsyncClient):
        """Test that oauth_state cookie has correct expiration time"""
        response = await client.get("/auth/oauth/google/authorize")

        assert response.status_code == 200
        set_cookie_header = response.headers.get("set-cookie", "")

        # Cookie should have Max-Age=600 (10 minutes)
        assert "Max-Age=600" in set_cookie_header

    async def test_multiple_requests_set_different_cookies(self, client: AsyncClient):
        """Test that multiple authorization requests set independent cookies"""
        # Make two separate requests
        response1 = await client.get("/auth/oauth/google/authorize")
        response2 = await client.get("/auth/oauth/google/authorize")

        assert response1.status_code == 200
        assert response2.status_code == 200

        state1 = response1.json()["state"]
        state2 = response2.json()["state"]
        cookie1 = response1.cookies["oauth_state"]
        cookie2 = response2.cookies["oauth_state"]

        # All values should be unique
        assert state1 != state2
        assert cookie1 != cookie2
        assert cookie1 == state1
        assert cookie2 == state2

    async def test_secure_cookie_flag_is_set(self, client: AsyncClient):
        """Test that oauth_state cookie has Secure flag set"""
        response = await client.get("/auth/oauth/google/authorize")

        assert response.status_code == 200
        set_cookie_header = response.headers.get("set-cookie", "")

        # Cookie should have Secure flag
        assert "Secure" in set_cookie_header or "secure" in set_cookie_header.lower()

    async def test_authorization_url_includes_redirect_uri(self, client: AsyncClient):
        """Test that authorization URL includes the correct redirect URI"""
        response = await client.get("/auth/oauth/google/authorize")

        assert response.status_code == 200
        auth_url = response.json()["authorization_url"]

        # Should contain redirect_uri parameter pointing to OAuth endpoint
        assert "redirect_uri=" in auth_url
        assert "/oauth/google" in auth_url


class TestGoogleCallbackEndpoint(BaseTest):
    """Tests for the Google OAuth callback endpoint"""

    async def test_successful_oauth_login_for_new_user(self, client: AsyncClient, mocker):
        """Test successful OAuth authentication for a new user"""
        # Arrange: Mock OAuth provider methods
        mock_access_token = "mock_google_access_token"
        mock_oauth_user_info = OAuthUserInfo(
            email="newuser@example.com",
            oauth_id="google_12345",
            first_name="John",
            second_name="Doe",
            email_verified=True,
        )

        mocker.patch.object(GoogleOAuthProvider, "exchange_code_for_token", return_value=mock_access_token)
        mocker.patch.object(GoogleOAuthProvider, "get_user_info", return_value=mock_oauth_user_info)

        # Set up state cookie
        state = "test_state_token"
        code = "test_authorization_code"

        # Act: Call callback endpoint with state cookie
        response = await client.get(
            f"/auth/oauth/google/callback?code={code}&state={state}", cookies={"oauth_state": state}
        )

        # Assert: Check response
        assert response.status_code == 200
        data = response.json()

        assert "access_token" in data
        assert data["access_token"] is not None
        assert data["token_type"] == "bearer"
        assert data["is_new_user"] is True

        # Check refresh token cookie is set
        assert "refresh" in response.cookies
        refresh_cookie = response.cookies["refresh"]
        assert refresh_cookie is not None
        assert refresh_cookie != ""

        # Verify oauth_state cookie is deleted
        set_cookie_header = response.headers.get("set-cookie", "")
        assert "oauth_state=" in set_cookie_header
        assert "Max-Age=0" in set_cookie_header or "Expires" in set_cookie_header

        # Verify user was created in database
        user = await self.get_user_by_email("newuser@example.com")
        assert user is not None
        assert user.oauth_provider == OAuthProvider.GOOGLE
        assert user.oauth_id == "google_12345"
        assert user.first_name == "John"
        assert user.second_name == "Doe"
        assert user.is_active is True  # OAuth users are auto-activated
        assert user.password is None  # OAuth users don't have passwords

    async def test_successful_oauth_login_for_existing_user(self, client: AsyncClient, mocker):
        """Test successful OAuth authentication for an existing OAuth user"""
        # Arrange: Create existing OAuth user
        _existing_user = await self.create_user(
            email="existing@example.com",
            oauth_provider=OAuthProvider.GOOGLE,
            oauth_id="google_67890",
            is_active=True,
            password=None,
        )

        mock_access_token = "mock_google_access_token"
        mock_oauth_user_info = OAuthUserInfo(
            email="existing@example.com",
            oauth_id="google_67890",
            first_name="Jane",
            second_name="Smith",
            email_verified=True,
        )

        mocker.patch.object(GoogleOAuthProvider, "exchange_code_for_token", return_value=mock_access_token)
        mocker.patch.object(GoogleOAuthProvider, "get_user_info", return_value=mock_oauth_user_info)

        state = "test_state_token"
        code = "test_authorization_code"

        # Act: Call callback endpoint
        response = await client.get(
            f"/auth/oauth/google/callback?code={code}&state={state}", cookies={"oauth_state": state}
        )

        # Assert: Check response
        assert response.status_code == 200
        data = response.json()

        assert "access_token" in data
        assert data["is_new_user"] is False

        # Check refresh token cookie is set
        assert "refresh" in response.cookies

    async def test_missing_state_cookie_returns_400(self, client: AsyncClient):
        """Test that missing oauth_state cookie returns 400 Bad Request"""
        # Act: Call callback without state cookie
        response = await client.get("/auth/oauth/google/callback?code=test_code&state=test_state")

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Missing state cookie"

    async def test_state_mismatch_returns_400(self, client: AsyncClient):
        """Test that state mismatch returns 400 Bad Request (CSRF protection)"""
        # Arrange: Set up mismatched state values
        cookie_state = "state_in_cookie"
        url_state = "different_state_in_url"

        # Act: Call callback with mismatched states
        response = await client.get(
            f"/auth/oauth/google/callback?code=test_code&state={url_state}", cookies={"oauth_state": cookie_state}
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "State mismatch - possible CSRF attack"

    async def test_token_exchange_error_returns_400(self, client: AsyncClient, mocker):
        """Test that OAuth token exchange errors return 400 Bad Request"""
        # Arrange: Mock token exchange failure
        mocker.patch.object(
            GoogleOAuthProvider,
            "exchange_code_for_token",
            side_effect=OAuthTokenExchangeError("Token exchange failed"),
        )

        state = "test_state_token"
        code = "invalid_code"

        # Act: Call callback endpoint
        response = await client.get(
            f"/auth/oauth/google/callback?code={code}&state={state}", cookies={"oauth_state": state}
        )

        # Assert
        assert response.status_code == 400
        assert "Token exchange failed" in response.json()["detail"]

    async def test_provider_error_returns_502(self, client: AsyncClient, mocker):
        """Test that OAuth provider errors return 502 Bad Gateway"""
        # Arrange: Mock successful token exchange but failed user info retrieval
        mock_access_token = "mock_access_token"
        mocker.patch.object(GoogleOAuthProvider, "exchange_code_for_token", return_value=mock_access_token)
        mocker.patch.object(
            GoogleOAuthProvider,
            "get_user_info",
            side_effect=OAuthProviderError("Failed to fetch user info"),
        )

        state = "test_state_token"
        code = "test_code"

        # Act: Call callback endpoint
        response = await client.get(
            f"/auth/oauth/google/callback?code={code}&state={state}", cookies={"oauth_state": state}
        )

        # Assert
        assert response.status_code == 502
        assert "Failed to fetch user info" in response.json()["detail"]

    async def test_account_already_linked_returns_409(self, client: AsyncClient, mocker):
        """Test that linking an OAuth account to a different email returns 409 Conflict"""
        # Arrange: Create existing OAuth user with different email
        await self.create_user(
            email="original@example.com",
            oauth_provider=OAuthProvider.GOOGLE,
            oauth_id="google_12345",
            is_active=True,
            password=None,
        )

        # Mock OAuth provider to return different email for same oauth_id
        mock_access_token = "mock_access_token"
        mock_oauth_user_info = OAuthUserInfo(
            email="different@example.com",  # Different email
            oauth_id="google_12345",  # Same OAuth ID
            email_verified=True,
        )

        mocker.patch.object(GoogleOAuthProvider, "exchange_code_for_token", return_value=mock_access_token)
        mocker.patch.object(GoogleOAuthProvider, "get_user_info", return_value=mock_oauth_user_info)

        state = "test_state_token"
        code = "test_code"

        # Act: Call callback endpoint
        response = await client.get(
            f"/auth/oauth/google/callback?code={code}&state={state}", cookies={"oauth_state": state}
        )

        # Assert
        assert response.status_code == 409
        assert "already linked to a different email" in response.json()["detail"]

    async def test_user_already_exists_with_local_account_links_oauth(self, client: AsyncClient, mocker):
        """Test that OAuth login for existing local account links the OAuth provider"""
        # Arrange: Create existing local user
        existing_user = await self.create_user(
            email="localuser@example.com",
            oauth_provider=OAuthProvider.LOCAL,
            is_active=True,
        )

        mock_access_token = "mock_access_token"
        mock_oauth_user_info = OAuthUserInfo(
            email="localuser@example.com",
            oauth_id="google_99999",
            email_verified=True,
        )

        mocker.patch.object(GoogleOAuthProvider, "exchange_code_for_token", return_value=mock_access_token)
        mocker.patch.object(GoogleOAuthProvider, "get_user_info", return_value=mock_oauth_user_info)

        state = "test_state_token"
        code = "test_code"

        # Act: Call callback endpoint
        response = await client.get(
            f"/auth/oauth/google/callback?code={code}&state={state}", cookies={"oauth_state": state}
        )

        # Assert: Check response
        assert response.status_code == 200
        data = response.json()
        assert data["is_new_user"] is False

        # Verify OAuth provider was linked to existing account
        assert existing_user.id is not None
        user = await self.get_user(existing_user.id)
        assert user is not None
        assert user.oauth_provider == OAuthProvider.GOOGLE
        assert user.oauth_id == "google_99999"

    async def test_generic_oauth_error_returns_400(self, client: AsyncClient, mocker):
        """Test that generic OAuth errors return 400 Bad Request"""
        # Arrange: Mock generic OAuth error
        mocker.patch.object(
            GoogleOAuthProvider,
            "exchange_code_for_token",
            side_effect=OAuthError("Generic OAuth error"),
        )

        state = "test_state_token"
        code = "test_code"

        # Act: Call callback endpoint
        response = await client.get(
            f"/auth/oauth/google/callback?code={code}&state={state}", cookies={"oauth_state": state}
        )

        # Assert
        assert response.status_code == 400
        assert "Generic OAuth error" in response.json()["detail"]

    async def test_refresh_token_cookie_attributes(self, client: AsyncClient, mocker):
        """Test that refresh token cookie has correct security attributes"""
        # Arrange
        mock_access_token = "mock_access_token"
        mock_oauth_user_info = OAuthUserInfo(
            email="testcookie@example.com",
            oauth_id="google_cookie_test",
            email_verified=True,
        )

        mocker.patch.object(GoogleOAuthProvider, "exchange_code_for_token", return_value=mock_access_token)
        mocker.patch.object(GoogleOAuthProvider, "get_user_info", return_value=mock_oauth_user_info)

        state = "test_state_token"
        code = "test_code"

        # Act
        response = await client.get(
            f"/auth/oauth/google/callback?code={code}&state={state}", cookies={"oauth_state": state}
        )

        # Assert
        assert response.status_code == 200

        # Check refresh token cookie attributes
        set_cookie_header = response.headers.get("set-cookie", "")
        assert "refresh=" in set_cookie_header
        assert "HttpOnly" in set_cookie_header
        assert "SameSite" in set_cookie_header or "samesite" in set_cookie_header.lower()

    async def test_oauth_state_cookie_is_deleted_after_callback(self, client: AsyncClient, mocker):
        """Test that oauth_state cookie is properly deleted after successful callback"""
        # Arrange
        mock_access_token = "mock_access_token"
        mock_oauth_user_info = OAuthUserInfo(
            email="deletecookie@example.com",
            oauth_id="google_delete_test",
            email_verified=True,
        )

        mocker.patch.object(GoogleOAuthProvider, "exchange_code_for_token", return_value=mock_access_token)
        mocker.patch.object(GoogleOAuthProvider, "get_user_info", return_value=mock_oauth_user_info)

        state = "test_state_token"
        code = "test_code"

        # Act
        response = await client.get(
            f"/auth/oauth/google/callback?code={code}&state={state}", cookies={"oauth_state": state}
        )

        # Assert
        assert response.status_code == 200

        # Verify oauth_state cookie deletion
        all_set_cookies = response.headers.get_list("set-cookie")
        oauth_state_cookie = [c for c in all_set_cookies if "oauth_state=" in c]
        assert len(oauth_state_cookie) > 0
        # Cookie should be deleted (Max-Age=0 or past Expires date)
        assert "Max-Age=0" in oauth_state_cookie[0] or "Expires" in oauth_state_cookie[0]

    async def test_missing_code_parameter_returns_422(self, client: AsyncClient):
        """Test that missing code parameter returns 422 Unprocessable Entity"""
        state = "test_state_token"

        # Act: Call callback without code parameter
        response = await client.get(f"/auth/oauth/google/callback?state={state}", cookies={"oauth_state": state})

        # Assert
        assert response.status_code == 422
        detail = response.json().get("detail", [])
        assert any("code" in str(d).lower() for d in detail)

    async def test_missing_state_parameter_returns_422(self, client: AsyncClient):
        """Test that missing state parameter returns 422 Unprocessable Entity"""
        code = "test_code"

        # Act: Call callback without state parameter
        response = await client.get(f"/auth/oauth/google/callback?code={code}", cookies={"oauth_state": "test_state"})

        # Assert
        assert response.status_code == 422
        detail = response.json().get("detail", [])
        assert any("state" in str(d).lower() for d in detail)

    async def test_oauth_user_auto_activated(self, client: AsyncClient, mocker):
        """Test that OAuth users are automatically activated (no email verification needed)"""
        # Arrange
        mock_access_token = "mock_access_token"
        mock_oauth_user_info = OAuthUserInfo(
            email="autoactivate@example.com",
            oauth_id="google_activate_test",
            email_verified=True,
        )

        mocker.patch.object(GoogleOAuthProvider, "exchange_code_for_token", return_value=mock_access_token)
        mocker.patch.object(GoogleOAuthProvider, "get_user_info", return_value=mock_oauth_user_info)

        state = "test_state_token"
        code = "test_code"

        # Act
        response = await client.get(
            f"/auth/oauth/google/callback?code={code}&state={state}", cookies={"oauth_state": state}
        )

        # Assert
        assert response.status_code == 200

        # Verify user is automatically activated
        user = await self.get_user_by_email("autoactivate@example.com")
        assert user is not None
        assert user.is_active is True

    async def test_oauth_user_has_no_password(self, client: AsyncClient, mocker):
        """Test that OAuth users are created without a password field"""
        # Arrange
        mock_access_token = "mock_access_token"
        mock_oauth_user_info = OAuthUserInfo(
            email="nopassword@example.com",
            oauth_id="google_nopass_test",
            email_verified=True,
        )

        mocker.patch.object(GoogleOAuthProvider, "exchange_code_for_token", return_value=mock_access_token)
        mocker.patch.object(GoogleOAuthProvider, "get_user_info", return_value=mock_oauth_user_info)

        state = "test_state_token"
        code = "test_code"

        # Act
        response = await client.get(
            f"/auth/oauth/google/callback?code={code}&state={state}", cookies={"oauth_state": state}
        )

        # Assert
        assert response.status_code == 200

        # Verify user has no password
        user = await self.get_user_by_email("nopassword@example.com")
        assert user is not None
        assert user.password is None

    async def test_response_matches_oauth_login_response_schema(self, client: AsyncClient, mocker):
        """Test that response matches OAuthLoginResponse schema"""
        # Arrange
        mock_access_token = "mock_access_token"
        mock_oauth_user_info = OAuthUserInfo(
            email="schema@example.com",
            oauth_id="google_schema_test",
            email_verified=True,
        )

        mocker.patch.object(GoogleOAuthProvider, "exchange_code_for_token", return_value=mock_access_token)
        mocker.patch.object(GoogleOAuthProvider, "get_user_info", return_value=mock_oauth_user_info)

        state = "test_state_token"
        code = "test_code"

        # Act
        response = await client.get(
            f"/auth/oauth/google/callback?code={code}&state={state}", cookies={"oauth_state": state}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()

        # Validate schema fields
        assert "access_token" in data
        assert "token_type" in data
        assert "is_new_user" in data
        assert isinstance(data["access_token"], str)
        assert data["token_type"] == "bearer"
        assert isinstance(data["is_new_user"], bool)
