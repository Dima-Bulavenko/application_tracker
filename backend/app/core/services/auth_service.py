from app.core.dto import AccessTokenPayload, RefreshTokenPayload, Token, TokenType, UserLogin
from app.core.exceptions import InvalidPasswordError, UserNotFoundError
from app.core.exceptions.user import UserNotActivatedError
from app.core.repositories import IUserRepository
from app.core.security import IPasswordHasher, ITokenStrategy
from app.core.services.refresh_token_service import RefreshTokenService

type TokenPairT = tuple[Token[AccessTokenPayload], Token[RefreshTokenPayload]]


class AuthService:
    def __init__(
        self,
        user_repo: IUserRepository,
        password_hasher: IPasswordHasher,
        access_strategy: ITokenStrategy[AccessTokenPayload],
        refresh_token_service: RefreshTokenService,
    ) -> None:
        self.user_repo = user_repo
        self.password_hasher = password_hasher
        self.access_strategy = access_strategy
        self.refresh_token_service = refresh_token_service

    async def login_with_credentials(self, user_creds: UserLogin) -> TokenPairT:
        user = await self.user_repo.get_by_email(user_creds.email)
        if not user or user.id is None:
            raise UserNotFoundError(f"User with {user_creds.email} does not exist")  # noqa: EM102
        if not user.is_active:
            raise UserNotActivatedError(f"User with {user_creds.email} is not activated")  # noqa: EM102
        if not self.password_hasher.verify(user_creds.password, user.password):
            raise InvalidPasswordError("Incorrect password")

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

    async def refresh_token(self, old_refresh_token: str, user_id: int | None = None) -> TokenPairT:
        """Refresh access and refresh tokens using strict rotation.

        Args:
            old_refresh_token: The raw refresh token from the client
            user_id: Optional user ID for additional validation. If not provided,
                    the user_id is extracted from the refresh token itself.

        Returns:
            New access and refresh token pair

        Raises:
            TokenInvalidError: Token not found or doesn't belong to user
            TokenExpireError: Token has expired
            RefreshTokenRevokedError: Token has been revoked
            RefreshTokenReuseError: Token has been used (potential attack)
            UserNotFoundError: User no longer exists
        """
        # Validate and rotate the refresh token (strict rotation with reuse detection)
        # Returns tuple of (new_raw_token, user_id)
        new_raw_refresh_token, token_user_id = await self.refresh_token_service.validate_and_rotate(
            old_refresh_token, user_id
        )

        # Get user for access token generation
        user = await self.user_repo.get_by_id(token_user_id)
        if not user or user.id is None:
            raise UserNotFoundError(f"User with id {token_user_id} does not exist")  # noqa: EM102

        # Generate new access token
        new_access_token = self.access_strategy.create_token(AccessTokenPayload(user_email=user.email, user_id=user.id))

        # Create new refresh token response object with payload metadata
        new_refresh_token = Token(
            token=new_raw_refresh_token,
            type=TokenType.refresh,
            payload=RefreshTokenPayload(user_email=user.email, user_id=user.id),
        )

        return new_access_token, new_refresh_token

    async def logout(self, refresh_token: str) -> None:
        """Revoke the provided refresh token."""
        await self.refresh_token_service.revoke(refresh_token)

    async def logout_all_devices(self, user_id: int) -> None:
        """Revoke all refresh tokens for a user (logout from all devices)."""
        await self.refresh_token_service.revoke_all_for_user(user_id)
