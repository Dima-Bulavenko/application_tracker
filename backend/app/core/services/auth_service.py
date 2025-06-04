from app.core.dto import UserRead
from app.core.exceptions import InvalidPasswordError, UserNotFoundError
from app.core.repositories import IUserRepository
from app.core.security import IPasswordHasher


class AuthService:
    def __init__(
        self,
        user_repo: IUserRepository,
        password_hasher: IPasswordHasher,
    ) -> None:
        self.user_repo = user_repo
        self.password_hasher = password_hasher

    async def authenticate(self, email: str, password) -> UserRead:
        user = await self.user_repo.get_by_email(email)
        # TODO: Check is user active to
        if not user:
            raise UserNotFoundError(f"User with {email} does not exist")  # noqa: EM102
        if not self.password_hasher.verify(password, user.password):
            raise InvalidPasswordError("Incorrect password")
        return UserRead.model_validate(user)
