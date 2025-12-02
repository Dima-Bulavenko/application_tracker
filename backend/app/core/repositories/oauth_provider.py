from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class OAuthUserInfo:
    """User information retrieved from OAuth provider"""

    email: str
    oauth_id: str
    first_name: str | None = None
    second_name: str | None = None
    email_verified: bool = False


class IOAuthProvider(ABC):
    """Abstract interface for OAuth providers"""

    @abstractmethod
    def get_authorization_url(self, state: str) -> str:
        """Generate authorization URL for OAuth flow

        Args:
            state: CSRF protection state token

        Returns:
            Authorization URL to redirect user to
        """
        ...

    @abstractmethod
    async def exchange_code_for_token(self, code: str, state: str) -> str:
        """Exchange authorization code for access token

        Args:
            code: Authorization code from OAuth callback
            state: CSRF protection state token

        Returns:
            Access token from OAuth provider

        Raises:
            OAuthTokenExchangeError: If token exchange fails
            OAuthStateMismatchError: If state validation fails
        """
        ...

    @abstractmethod
    async def get_user_info(self, access_token: str) -> OAuthUserInfo:
        """Fetch user information using access token

        Args:
            access_token: OAuth access token

        Returns:
            User information from OAuth provider

        Raises:
            OAuthProviderError: If user info retrieval fails
        """
        ...
