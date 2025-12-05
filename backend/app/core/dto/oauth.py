from typing import Literal

from pydantic import Field

from .config import BaseModelDTO


class OAuthCallbackRequest(BaseModelDTO):
    """OAuth callback request with authorization code and state"""

    code: str = Field(description="Authorization code from OAuth provider")
    state: str = Field(description="CSRF protection state token")


class OAuthLoginResponse(BaseModelDTO):
    """OAuth login/signup response with JWT tokens"""

    access_token: str = Field(description="JWT access token")
    token_type: Literal["bearer"] = Field(default="bearer", description="Token type")
    is_new_user: bool = Field(description="Whether this is a new user registration")


class OAuthAuthorizeResponse(BaseModelDTO):
    """OAuth authorization URL response"""

    authorization_url: str = Field(description="URL to redirect user to for OAuth authorization")
    state: str = Field(description="CSRF protection state token")
