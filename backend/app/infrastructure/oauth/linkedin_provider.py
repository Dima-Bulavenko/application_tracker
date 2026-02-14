from __future__ import annotations

import httpx

from app import LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, OAUTH_REDIRECT_URI
from app.core.domain.user import OAuthProvider
from app.core.exceptions.oauth import OAuthProviderError, OAuthTokenExchangeError
from app.core.repositories.oauth_provider import IOAuthProvider, OAuthStateProvider, OAuthUserInfo


class LinkedInOAuthProvider(IOAuthProvider):
    """LinkedIn OAuth2 provider implementation"""

    __type = OAuthProvider.LINKEDIN
    AUTHORIZATION_URL = "https://www.linkedin.com/oauth/v2/authorization"
    TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
    USERINFO_URL = "https://api.linkedin.com/v2/userinfo"

    def __init__(self):
        self.client_id = LINKEDIN_CLIENT_ID
        self.client_secret = LINKEDIN_CLIENT_SECRET
        self.redirect_uri = f"{OAUTH_REDIRECT_URI}/linkedin"
        self.__state_provider = OAuthStateProvider()

    def get_authorization_url(self) -> str:
        """Generate LinkedIn OAuth authorization URL"""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "openid profile email",
            "state": self.state,
        }
        query_string = "&".join([f"{key}={value}" for key, value in params.items()])
        return f"{self.AUTHORIZATION_URL}?{query_string}"

    async def exchange_code_for_token(self, code: str) -> str:
        """Exchange authorization code for access token"""
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.TOKEN_URL, data=data)
                response.raise_for_status()
                token_data = response.json()
                return token_data["access_token"]
            except (httpx.HTTPError, KeyError) as e:
                raise OAuthTokenExchangeError(f"Failed to exchange code for token: {e}") from e

    async def get_user_info(self, access_token: str) -> OAuthUserInfo:
        """Fetch user information from LinkedIn"""
        headers = {"Authorization": f"Bearer {access_token}"}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.USERINFO_URL, headers=headers)
                response.raise_for_status()
                user_data = response.json()

                return OAuthUserInfo(
                    email=user_data["email"],
                    oauth_id=user_data["sub"],
                    first_name=user_data.get("given_name"),
                    second_name=user_data.get("family_name"),
                    email_verified=user_data.get("email_verified", False),
                )
            except (httpx.HTTPError, KeyError) as e:
                raise OAuthProviderError(f"Failed to fetch user info from LinkedIn: {e}") from e

    @property
    def type(self) -> OAuthProvider:
        return self.__type

    @property
    def state(self) -> str:
        """Get or generate state token for CSRF protection"""
        return self.__state_provider.state
