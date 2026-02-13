from __future__ import annotations

import httpx

from app import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, OAUTH_REDIRECT_URI
from app.core.exceptions.oauth import OAuthProviderError, OAuthTokenExchangeError
from app.core.repositories.oauth_provider import IOAuthProvider, OAuthUserInfo


class GoogleOAuthProvider(IOAuthProvider):
    """Google OAuth2 provider implementation"""

    AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

    def __init__(self):
        self.client_id = GOOGLE_CLIENT_ID
        self.client_secret = GOOGLE_CLIENT_SECRET
        self.redirect_uri = f"{OAUTH_REDIRECT_URI}/google"

    def get_authorization_url(self, state: str, code_challenge: str, code_challenge_method: str = "S256") -> str:
        """Generate Google OAuth authorization URL"""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "access_type": "offline",
            "prompt": "consent",
            "code_challenge": code_challenge,
            "code_challenge_method": code_challenge_method,
        }
        query_string = "&".join([f"{key}={value}" for key, value in params.items()])
        return f"{self.AUTHORIZATION_URL}?{query_string}"

    async def exchange_code_for_token(self, code: str, code_verifier: str) -> str:
        """Exchange authorization code for access token"""
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
            "code_verifier": code_verifier,
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
        """Fetch user information from Google"""
        headers = {"Authorization": f"Bearer {access_token}"}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.USERINFO_URL, headers=headers)
                response.raise_for_status()
                user_data = response.json()

                return OAuthUserInfo(
                    email=user_data["email"],
                    oauth_id=user_data["id"],
                    first_name=user_data.get("given_name"),
                    second_name=user_data.get("family_name"),
                    email_verified=user_data.get("verified_email", False),
                )
            except (httpx.HTTPError, KeyError) as e:
                raise OAuthProviderError(f"Failed to fetch user info from Google: {e}") from e
