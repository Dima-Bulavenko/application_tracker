from app.core.dto import AuthTokenPair, UserLogin
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

    async def login_with_credentials(self, user_creds: UserLogin) -> AuthTokenPair:
        user = await self.user_repo.get_by_email(user_creds.email)
        # TODO: Check is user active to
        if not user:
            raise UserNotFoundError(f"User with {user_creds.email} does not exist")  # noqa: EM102
        if not self.password_hasher.verify(user_creds.password, user.password):
            raise InvalidPasswordError("Incorrect password")

        access_token = self.token_provider.create_refresh_token(user)
        refresh_token = self.token_provider.create_refresh_token(user)
        return AuthTokenPair(access=access_token, refresh=refresh_token)
