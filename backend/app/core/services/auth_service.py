from app.core.dto import AccessTokenPayload, RefreshTokenPayload, Token, UserLogin
from app.core.exceptions import InvalidPasswordError, UserNotFoundError
from app.core.repositories import IUserRepository
from app.core.security import IPasswordHasher, ITokenStrategy

type TokenPairT = tuple[Token[AccessTokenPayload], Token[RefreshTokenPayload]]


class AuthService:
    def __init__(
        self,
        user_repo: IUserRepository,
        password_hasher: IPasswordHasher,
        access_strategy: ITokenStrategy[AccessTokenPayload],
        refresh_strategy: ITokenStrategy[RefreshTokenPayload],
    ) -> None:
        self.user_repo = user_repo
        self.password_hasher = password_hasher
        self.access_strategy = access_strategy
        self.refresh_strategy = refresh_strategy

    async def login_with_credentials(self, user_creds: UserLogin) -> TokenPairT:
        user = await self.user_repo.get_by_email(user_creds.email)
        # TODO: Check is user active to
        if not user or user.id is None:
            raise UserNotFoundError(f"User with {user_creds.email} does not exist")  # noqa: EM102
        if not self.password_hasher.verify(user_creds.password, user.password):
            raise InvalidPasswordError("Incorrect password")

        access_token = self.access_strategy.create_token(AccessTokenPayload(user_email=user.email, user_id=user.id))
        refresh_token = self.refresh_strategy.create_token(RefreshTokenPayload(user_email=user.email, user_id=user.id))
        return access_token, refresh_token

    async def refresh_token(self, old_refresh_token: str) -> TokenPairT:
        # TODO: Implement token blacklisting
        refresh_token = self.refresh_strategy.verify_token(old_refresh_token)

        user = await self.user_repo.get_by_email(refresh_token.payload.user_email)
        if not user or user.id is None:
            raise UserNotFoundError(f"User with {user.email} email does not exist")  # noqa: EM102

        new_access_token = self.access_strategy.create_token(AccessTokenPayload(user_email=user.email, user_id=user.id))
        new_refresh_token = self.refresh_strategy.create_token(
            RefreshTokenPayload(user_email=user.email, user_id=user.id)
        )

        return new_access_token, new_refresh_token

    async def logout(self, access_token: str, refresh_token: str) -> TokenPairT:
        # TODO: Implement token blacklisting
        access_token_v = self.access_strategy.verify_token(access_token)
        refresh_token_v = self.refresh_strategy.verify_token(refresh_token)

        try:
            await self.user_repo.get_by_email(access_token_v.payload.user_email)
        except UserNotFoundError as e:
            message = f"User with {refresh_token_v.payload.user_email} email does not exist"
            raise UserNotFoundError(message) from e
        return access_token_v, refresh_token_v
