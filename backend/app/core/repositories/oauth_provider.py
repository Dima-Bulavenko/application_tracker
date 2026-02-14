import base64
import hashlib
import secrets
from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.core.domain.user import OAuthProvider


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
    def get_authorization_url(self) -> str:
        """Generate authorization URL for OAuth flow

        Returns:
            Authorization URL to redirect user to
        """
        ...

    @abstractmethod
    async def exchange_code_for_token(self, code: str) -> str:
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

    @property
    @abstractmethod
    def type(self) -> OAuthProvider:
        """OAuth provider type enum"""
        ...


class OAuthStateProvider:
    """Generate state tokens for CSRF protection"""

    def __init__(self) -> None:
        self.__state = secrets.token_urlsafe(32)

    @property
    def state(self) -> str:
        """Get state token for CSRF protection"""
        return self.__state


class OAuthPKCEProvider:
    """Provide PKCE protection for OAuth flows"""

    def __init__(self, code_verifier: str | None = None) -> None:
        self.__code_verifier = code_verifier
        self.__code_challenge: str | None = None

    @staticmethod
    def _generate_code_verifier() -> str:
        """Generate a secure random code verifier"""
        return secrets.token_urlsafe(64)

    @staticmethod
    def _generate_code_challenge(verifier: str) -> str:
        """Generate code challenge from code verifier"""

        sha256 = hashlib.sha256(verifier.encode()).digest()
        return base64.urlsafe_b64encode(sha256).rstrip(b"=").decode()

    @property
    def code_verifier(self) -> str:
        """Get or generate code verifier for PKCE"""
        if self.__code_verifier is None:
            self.__code_verifier = self._generate_code_verifier()
        return self.__code_verifier

    @property
    def code_challenge(self) -> str:
        """Generate code challenge from code verifier"""
        if self.__code_challenge is None:
            self.__code_challenge = self._generate_code_challenge(self.code_verifier)
        return self.__code_challenge

    @property
    def code_challenge_method(self) -> str:
        """PKCE code challenge method"""
        return "S256"
