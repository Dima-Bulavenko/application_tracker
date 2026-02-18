import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain import User
from app.core.dto import AccessTokenPayload, RefreshTokenPayload, Token, TokenType
from app.core.security import ITokenStrategy
from app.core.services import RefreshTokenService
from app.infrastructure.repositories import RefreshTokenSQLAlchemyRepository


@pytest.fixture
def access_token_factory(access_token_strategy: ITokenStrategy[AccessTokenPayload]):
    """Factory for creating access tokens."""

    def create_access_token(user: User) -> Token[AccessTokenPayload]:
        """
        Create an access token for a user.

        Args:
            user: User domain object

        Returns:
            Token[AccessTokenPayload]: Access token with payload
        """
        assert user.id is not None, "User ID must be set to create access token"
        payload = AccessTokenPayload(user_email=user.email, user_id=user.id)
        return access_token_strategy.create_token(payload)

    return create_access_token


@pytest.fixture
def refresh_token_factory(session: AsyncSession):
    """Factory for creating refresh tokens."""

    async def create_refresh_token(user: User) -> Token[RefreshTokenPayload]:
        """
        Create a database-backed refresh token for a user.

        Args:
            user: User domain object

        Returns:
            Token[RefreshTokenPayload]: Refresh token with payload
        """
        assert user.id is not None, "User ID must be set to create refresh token"
        refresh_token_repo = RefreshTokenSQLAlchemyRepository(session)
        service = RefreshTokenService(refresh_token_repo)
        raw_token = await service.issue(user.id)

        # Return Token object with raw token and payload for compatibility
        payload = RefreshTokenPayload(user_email=user.email, user_id=user.id)
        return Token(token=raw_token, type=TokenType.refresh, payload=payload)

    return create_refresh_token
