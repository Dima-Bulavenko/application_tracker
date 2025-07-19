from __future__ import annotations

from app.core.domain import Application, Company
from app.core.dto import ApplicationCreate, ApplicationRead
from app.core.repositories import (
    IApplicationRepository,
    ICompanyRepository,
    IUserRepository,
)


class ApplicationService:
    def __init__(
        self,
        app_repo: IApplicationRepository,
        user_repo: IUserRepository,
        company_repo: ICompanyRepository,
    ) -> None:
        self.app_repo = app_repo
        self.user_repo = user_repo
        self.company_repo = company_repo

    async def get_applications_by_user_email(
        self, email: str, limit: int | None = None, offset: int | None = None
    ) -> list[ApplicationRead]:
        applications = await self.app_repo.get_by_user_email(email, limit, offset)
        return [ApplicationRead.model_validate(app) for app in applications]

    async def create(self, app: ApplicationCreate, user_id: int):
        company = await self.company_repo.get_by_name(app.company.name)
        if company is None:
            company = await self.company_repo.create(
                Company.model_validate(app.company, from_attributes=True)
            )
        app_dict = app.model_dump()
        app_dict.update({"company_id": company.id})
        app_dict.update({"user_id": user_id})
        application = await self.app_repo.create(Application.model_validate(app_dict))

        return ApplicationRead.model_validate(application, from_attributes=True)
