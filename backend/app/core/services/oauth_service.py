from __future__ import annotations

import base64
import hashlib
import secrets

from app.core.domain import User
from app.core.domain.user import OAuthProvider
from app.core.dto import AccessTokenPayload, RefreshTokenPayload, Token, TokenType
from app.core.exceptions.oauth import OAuthAccountAlreadyLinkedError, OAuthAccountAlreadyLinkedToProviderError
from app.core.repositories import IOAuthProvider, IUserRepository, OAuthUserInfo
from app.core.security import ITokenStrategy
from app.core.services.refresh_token_service import RefreshTokenService

type TokenPairT = tuple[Token[AccessTokenPayload], Token[RefreshTokenPayload]]


class OAuthService:
    """Service for handling OAuth authentication flow"""

    def __init__(
        self,
        user_repo: IUserRepository,
        access_strategy: ITokenStrategy[AccessTokenPayload],
        refresh_token_service: RefreshTokenService,
    ) -> None:
        self.user_repo = user_repo
        self.access_strategy = access_strategy
        self.refresh_token_service = refresh_token_service

    def generate_state_token(self) -> str:
        """Generate CSRF protection state token"""
        return secrets.token_urlsafe(32)

    def generate_code_verifier(self) -> str:
        """Generate code verified for PKCE protection"""
        return secrets.token_urlsafe(64)

    def generate_code_challenge(self, verifier: str) -> str:
        """Generate code challenge for PKCE protection"""
        sha256 = hashlib.sha256(verifier.encode()).digest()
        return base64.urlsafe_b64encode(sha256).rstrip(b"=").decode()

    async def authenticate_oauth_user(
        self, oauth_provider: IOAuthProvider, provider_type: OAuthProvider, code: str, state: str, code_verifier: str
    ) -> tuple[TokenPairT, bool]:
        """Authenticate or register user via OAuth

        Args:
            oauth_provider: OAuth provider implementation
            provider_type: OAuth provider type enum
            code: Authorization code from OAuth callback
            state: CSRF protection state token

        Returns:
            Tuple of (token_pair, is_new_user)
            - token_pair: Access and refresh tokens
            - is_new_user: True if this is a new registration, False if existing user

        Raises:
            OAuthTokenExchangeError: If token exchange fails
            OAuthProviderError: If user info retrieval fails
            OAuthAccountAlreadyLinkedError: If OAuth account linked to different email
        """
        # Exchange code for access token
        access_token = await oauth_provider.exchange_code_for_token(code, code_verifier)

        # Get user info from provider
        oauth_user_info = await oauth_provider.get_user_info(access_token)

        # Check if OAuth account already exists
        existing_oauth_user = await self.user_repo.get_by_oauth_id(provider_type, oauth_user_info.oauth_id)

        if existing_oauth_user:
            # OAuth account exists - verify email matches
            if existing_oauth_user.email != oauth_user_info.email:
                raise OAuthAccountAlreadyLinkedError(
                    f"This {provider_type.value} account is already linked to a different email"
                )

            # Login existing user
            tokens = await self._issue_tokens(existing_oauth_user)
            return tokens, False

        # Check if user with this email already exists (with different OAuth provider or local)
        existing_email_user = await self.user_repo.get_by_email(oauth_user_info.email)

        if existing_email_user:
            # Email exists - check if it's a local account or different OAuth provider
            if existing_email_user.oauth_provider == OAuthProvider.LOCAL:
                # Link OAuth to existing local account
                await self._link_oauth_to_user(existing_email_user, provider_type, oauth_user_info)
                tokens = await self._issue_tokens(existing_email_user)
                return tokens, False
            else:
                # User exists with different OAuth provider
                provider = existing_email_user.oauth_provider.value.capitalize()
                raise OAuthAccountAlreadyLinkedToProviderError(
                    f"This account was created with {provider}. Please use {provider} to sign in."
                )

        # Create new OAuth user
        new_user = await self._create_oauth_user(provider_type, oauth_user_info)
        tokens = await self._issue_tokens(new_user)
        return tokens, True

    async def _create_oauth_user(self, provider_type: OAuthProvider, oauth_info: OAuthUserInfo) -> User:
        """Create a new user from OAuth information"""
        user = User(
            email=oauth_info.email,
            password=None,  # OAuth users don't have passwords
            oauth_provider=provider_type,
            oauth_id=oauth_info.oauth_id,
            first_name=oauth_info.first_name,
            second_name=oauth_info.second_name,
            is_active=True,  # OAuth users are automatically activated if email is verified
        )
        return await self.user_repo.create(user)

    async def _link_oauth_to_user(self, user: User, provider_type: OAuthProvider, oauth_info: OAuthUserInfo) -> User:
        """Link OAuth account to existing user"""
        if user.id is None:
            raise ValueError("User ID is required to link OAuth account")

        updated_user = await self.user_repo.update(
            user.id,
            oauth_provider=provider_type,
            oauth_id=oauth_info.oauth_id,
            is_active=True,  # Activate user if linking OAuth
        )

        if not updated_user:
            raise ValueError(f"Failed to link OAuth account to user {user.id}")

        return updated_user

    async def _issue_tokens(self, user: User) -> TokenPairT:
        """Issue access and refresh tokens for user"""
        if user.id is None:
            raise ValueError("User ID is required to issue tokens")

        # Generate access token
        access_token = self.access_strategy.create_token(AccessTokenPayload(user_email=user.email, user_id=user.id))

        # Issue a new refresh token (stored in database)
        raw_refresh_token = await self.refresh_token_service.issue(user.id)

        # Create refresh token response object with payload metadata
        refresh_token = Token(
            token=raw_refresh_token,
            type=TokenType.refresh,
            payload=RefreshTokenPayload(user_email=user.email, user_id=user.id),
        )

        return access_token, refresh_token
