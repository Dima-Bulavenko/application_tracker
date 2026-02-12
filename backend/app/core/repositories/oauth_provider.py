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
    def get_authorization_url(self, state: str, code_challenge: str, code_challenge_method: str) -> str:
        """Generate authorization URL for OAuth flow

        Args:
            state: CSRF protection state token
            code_challenge: Challenge code for PKCE protection
            code_challenge_method: Hashing method that was used to get code challenge

        Returns:
            Authorization URL to redirect user to
        """
        ...

    @abstractmethod
    async def exchange_code_for_token(self, code: str, code_verifier: str) -> str:
        """Exchange authorization code for access token

        Args:
            code: Authorization code from OAuth callback
            code_verifier: code verifier for PKCE protection

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
