from __future__ import annotations

from sqlalchemy import select

from app.core.domain import Application
from app.core.repositories import IApplicationRepository
from app.db.models import Application as ApplicationModel
from app.db.models import User

from .config import SQLAlchemyRepository


class ApplicationSQLAlchemyRepository(
    SQLAlchemyRepository[ApplicationModel], IApplicationRepository
):
    model = ApplicationModel

    async def create(self, application: Application) -> Application:
        app_model = self.model(**application.model_dump())
        self.session.add(app_model)
        await self.session.flush()
        return Application.model_validate(app_model, from_attributes=True)

    async def get_by_user_email(
        self, email: str, limit: int | None = None, offset: int | None = None
    ) -> list[Application]:
        statement = (
            select(self.model)
            .join(User)
            .where(User.email == email)
            .limit(limit)
            .offset(offset)
        )
        apps = await self.session.scalars(statement)
        return [Application.model_validate(app, from_attributes=True) for app in apps]
