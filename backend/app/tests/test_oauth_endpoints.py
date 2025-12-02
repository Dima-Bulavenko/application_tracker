import re

from httpx import AsyncClient

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
        assert "SameSite=lax" in set_cookie_header or "samesite=lax" in set_cookie_header.lower()
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

        # Should contain redirect_uri parameter pointing to callback endpoint
        assert "redirect_uri=" in auth_url
        assert "google/callback" in auth_url
