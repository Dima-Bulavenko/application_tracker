from __future__ import annotations

from app.core.domain import Application
from app.core.repositories import IApplicationRepository
from app.db.models import Application as ApplicationModel

from .config import SQLAlchemyRepository


class ApplicationSQLAlchemyRepository(
    SQLAlchemyRepository[ApplicationModel], IApplicationRepository
):
    model = ApplicationModel

    async def create(self, application: Application) -> Application:
        app_model = await self._save(self.model(**application.model_dump()))

        return Application.model_validate(app_model, from_attributes=True)

    async def get_by_user_email(
        self, email: str, limit: int | None = None, offset: int | None = None
    ) -> list[Application]:
        model_applications = await self._get(limit=limit, offset=offset, email=email)
        return [
            Application.model_validate(app, from_attributes=True)
            for app in model_applications
        ]
