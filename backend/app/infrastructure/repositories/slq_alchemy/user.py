from __future__ import annotations

from sqlalchemy import delete, select, update

from app.core.domain import User
from app.core.domain.user import OAuthProvider
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

    async def get_by_oauth_id(self, oauth_provider: OAuthProvider, oauth_id: str) -> User | None:
        statement = select(self.model).where(
            self.model.oauth_provider == oauth_provider.value, self.model.oauth_id == oauth_id
        )
        user = await self.session.scalar(statement)
        return User.model_validate(user, from_attributes=True) if user else None

    async def get_by_email_and_provider(self, email: str, oauth_provider: OAuthProvider) -> User | None:
        statement = select(self.model).where(
            self.model.email == email, self.model.oauth_provider == oauth_provider.value
        )
        user = await self.session.scalar(statement)
        return User.model_validate(user, from_attributes=True) if user else None

    async def update(self, user_id: int, **update_data) -> User | None:
        statement = update(self.model).where(self.model.id == user_id).values(update_data).returning(self.model)
        updated_user = await self.session.scalar(statement)
        return User.model_validate(updated_user, from_attributes=True) if updated_user else None

    async def create(self, user: User) -> User:
        user_model = self.model(**user.model_dump(exclude_computed_fields=True))
        self.session.add(user_model)
        await self.session.flush()
        return User.model_validate(user_model, from_attributes=True)

    async def delete(self, user_id: int) -> User | None:
        statement = delete(self.model).where(self.model.id == user_id).returning(self.model)
        deleted_user = await self.session.scalar(statement)
        return User.model_validate(deleted_user, from_attributes=True) if deleted_user else None
