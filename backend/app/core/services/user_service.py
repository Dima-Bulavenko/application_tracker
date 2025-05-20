from app.core.domain import User
from app.core.dto.user import UserCreate, UserRead
from app.core.repositories import IUserRepository
from app.core.security import IPasswordHasher


class UserService:
    def __init__(
        self, user_repo: IUserRepository, password_hasher: IPasswordHasher
    ) -> None:
        self.user_repo = user_repo
        self.password_hasher = password_hasher

    async def create(self, user_data: UserCreate) -> UserRead:
        user_data.password = self.password_hasher.hash(user_data.password)
        user = await self.user_repo.save(User(user_data.email, user_data.password))
        return UserRead.model_validate(user, from_attributes=True)
