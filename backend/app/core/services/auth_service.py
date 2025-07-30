from app.core.dto import AccessToken, RefreshToken, UserLogin
from app.core.exceptions import InvalidPasswordError, UserNotFoundError
from app.core.repositories import IUserRepository
from app.core.security import IPasswordHasher, ITokenProvider


class AuthService:
    def __init__(
        self,
        user_repo: IUserRepository,
        password_hasher: IPasswordHasher,
        token_provider: ITokenProvider,
    ) -> None:
        self.user_repo = user_repo
        self.password_hasher = password_hasher
        self.token_provider = token_provider

    async def login_with_credentials(self, user_creds: UserLogin) -> tuple[AccessToken, RefreshToken]:
        user = await self.user_repo.get_by_email(user_creds.email)
        # TODO: Check is user active to
        if not user:
            raise UserNotFoundError(f"User with {user_creds.email} does not exist")  # noqa: EM102
        if not self.password_hasher.verify(user_creds.password, user.password):
            raise InvalidPasswordError("Incorrect password")

        access_token = self.token_provider.create_access_token(user)
        refresh_token = self.token_provider.create_refresh_token(user)
        return access_token, refresh_token

    async def refresh_token(self, old_refresh_token: str) -> tuple[AccessToken, RefreshToken]:
        # TODO: Implement token blacklisting
        refresh_token = self.token_provider.verify_refresh_token(old_refresh_token)

        user = await self.user_repo.get_by_email(refresh_token.payload.user_email)

        if not user:
            raise UserNotFoundError(f"User with {user.email} email does not exist")  # noqa: EM102

        new_access_token = self.token_provider.create_access_token(user)
        new_refresh_token = self.token_provider.create_refresh_token(user)

        return new_access_token, new_refresh_token

    async def logout(self, access_token: str, refresh_token: str) -> tuple[AccessToken, RefreshToken]:
        # TODO: Implement token blacklisting
        access_token_v = self.token_provider.verify_access_token(access_token)
        refresh_token_v = self.token_provider.verify_refresh_token(refresh_token)

        try:
            await self.user_repo.get_by_email(access_token_v.payload.user_email)
        except UserNotFoundError as e:
            message = f"User with {refresh_token_v.payload.user_email} email does not exist"
            raise UserNotFoundError(message) from e
        return access_token_v, refresh_token_v
