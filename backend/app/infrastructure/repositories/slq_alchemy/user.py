from __future__ import annotations

from sqlalchemy import select, update

from app.core.domain import User
from app.core.repositories import IUserRepository
from app.db.models import User as UserModel

from .config import SQLAlchemyRepository


class UserSQLAlchemyRepository(SQLAlchemyRepository[UserModel], IUserRepository):
    model = UserModel

    async def get_by_email(self, email: str) -> User | None:
        statement = select(self.model).where(self.model.email == email)
        user = await self.session.scalar(statement)
        return User.model_validate(user, from_attributes=True) if user else None

    async def get_by_id(self, user_id: int) -> User | None:
        statement = select(self.model).where(self.model.id == user_id)
        user = await self.session.scalar(statement)
        return User.model_validate(user, from_attributes=True) if user else None

    async def update(self, user_id: int, **update_data) -> User | None:
        statement = update(self.model).where(self.model.id == user_id).values(update_data).returning(self.model)
        updated_user = await self.session.scalar(statement)
        return User.model_validate(updated_user, from_attributes=True) if updated_user else None

    async def create(self, user: User) -> User:
        user_model = self.model(**user.model_dump())
        self.session.add(user_model)
        await self.session.flush()
        return User.model_validate(user_model, from_attributes=True)
