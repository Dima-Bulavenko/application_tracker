from __future__ import annotations

from sqlalchemy import update

from app.core.domain import User
from app.core.exceptions.user import UserAlreadyExistError, UserNotFoundError
from app.core.repositories import IUserRepository
from app.db.models import User as UserModel

from .config import SQLAlchemyMapper, SQLAlchemyRepository

mapper = SQLAlchemyMapper[User, UserModel](User, UserModel)


class UserSQLAlchemyRepository(SQLAlchemyRepository[UserModel], IUserRepository):
    model = UserModel

    async def __get_one(self, **kwargs):
        error_message = f"User with {', '.join((f'{k} = {v}' for k, v in kwargs.items()))}"
        item = await super()._get_one(error_message, UserNotFoundError, **kwargs)
        return item

    async def get_by_email(self, email: str) -> User:
        user = await self.__get_one(email=email)
        return mapper.to_domain(user)

    async def get_by_id(self, user_id: int) -> User:
        user = await self.__get_one(id=user_id)
        return mapper.to_domain(user)

    async def update(self, user_id: int, **update_data) -> User | None:
        statement = update(self.model).where(self.model.id == user_id).values(update_data).returning(self.model)
        updated_user = await self.session.scalar(statement)
        return mapper.to_domain(updated_user) if updated_user else None

    async def save(self, user: User) -> User:
        error_massage = f"User with {user.email} already exist"
        user_model = await self._save(mapper.to_repo(user), error_massage, UserAlreadyExistError)
        return mapper.to_domain(user_model)
