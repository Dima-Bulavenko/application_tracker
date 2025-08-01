from __future__ import annotations

from sqlalchemy import delete, select, update

from app.core.domain import Application
from app.core.repositories import IApplicationRepository
from app.db.models import Application as ApplicationModel
from app.db.models import User

from .config import SQLAlchemyRepository


class ApplicationSQLAlchemyRepository(SQLAlchemyRepository[ApplicationModel], IApplicationRepository):
    model = ApplicationModel

    async def create(self, application: Application) -> Application:
        app_model = self.model(**application.model_dump())
        self.session.add(app_model)
        await self.session.flush()
        return Application.model_validate(app_model, from_attributes=True)

    async def get_by_user_email(
        self, email: str, limit: int | None = None, offset: int | None = None
    ) -> list[Application]:
        statement = select(self.model).join(User).where(User.email == email).limit(limit).offset(offset)
        apps = await self.session.scalars(statement)
        return [Application.model_validate(app, from_attributes=True) for app in apps]

    async def get_by_id(self, application_id: int) -> Application | None:
        statement = select(self.model).where(self.model.id == application_id)
        app = await self.session.scalar(statement)
        return Application.model_validate(app, from_attributes=True) if app else None

    async def update(self, application_id: int, **update_data) -> Application:
        statement = update(self.model).where(self.model.id == application_id).values(update_data).returning(self.model)
        updated_app = await self.session.scalar(statement)
        return Application.model_validate(updated_app, from_attributes=True)

    async def delete(self, application_id: int) -> None:
        statement = delete(self.model).where(self.model.id == application_id)
        await self.session.execute(statement)
