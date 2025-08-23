from __future__ import annotations

from datetime import datetime

from app.core.domain import Application, Company
from app.core.dto import (
    ApplicationCreate,
    ApplicationFilterParams,
    ApplicationRead,
    ApplicationReadWithCompany,
    ApplicationUpdate,
    CompanyRead,
)
from app.core.exceptions import ApplicationNotFoundError, UserNotAuthorizedError
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
        self, email: str, filter_param: ApplicationFilterParams
    ) -> list[ApplicationReadWithCompany]:
        applications = await self.app_repo.get_by_user_email(email, filter_param)
        if not applications:
            return []
        companies_ids = {app.company_id for app in applications}
        companies = await self.company_repo.get_by_ids(companies_ids)
        companies_dict = {company.id: company for company in companies}
        return [
            ApplicationReadWithCompany(
                **app.model_dump(),
                company=CompanyRead.model_validate(companies_dict[app.company_id]),
            )
            for app in applications
        ]

    async def create(self, app: ApplicationCreate, user_id: int):
        company = await self.company_repo.get_by_name(app.company.name)
        if company is None:
            company = await self.company_repo.create(Company.model_validate(app.company, from_attributes=True))
        app_dict = app.model_dump()
        app_dict.update({"company_id": company.id})
        app_dict.update({"user_id": user_id})
        application = await self.app_repo.create(Application.model_validate(app_dict))

        return ApplicationRead.model_validate(application, from_attributes=True)

    async def update(self, application_id: int, app: ApplicationUpdate, user_id: int) -> ApplicationRead:
        existing_app = await self.app_repo.get_by_id(application_id)
        if not existing_app:
            raise ApplicationNotFoundError(f"Application with {application_id} id is not found")

        if existing_app.user_id != user_id:
            raise UserNotAuthorizedError(f"User with {user_id} id is not authorized to update this application")
        update_data = app.model_dump(exclude_unset=True)
        if not update_data:
            return ApplicationRead.model_validate(existing_app, from_attributes=True)

        if update_data.get("company"):
            company = await self.company_repo.get_by_name(update_data["company"]["name"])
            if company is None:
                company = await self.company_repo.create(Company(name=update_data["company"]["name"]))
            update_data["company_id"] = company.id
            update_data.pop("company")
        update_data["time_update"] = datetime.now()

        updated_app = await self.app_repo.update(application_id, **update_data)

        return ApplicationRead.model_validate(updated_app, from_attributes=True)

    async def get_by_id(self, application_id: int, user_id: int) -> ApplicationRead:
        """Get a single application by ID. User can only access their own applications."""
        existing_app = await self.app_repo.get_by_id(application_id)
        if not existing_app:
            raise ApplicationNotFoundError(f"Application with {application_id} id is not found")

        if existing_app.user_id != user_id:
            raise UserNotAuthorizedError(f"User with {user_id} id is not authorized to access this application")

        return ApplicationRead.model_validate(existing_app, from_attributes=True)

    async def delete(self, application_id: int, user_id: int) -> None:
        existing_app = await self.app_repo.get_by_id(application_id)
        if not existing_app:
            raise ApplicationNotFoundError(f"Application with {application_id} id is not found")

        if existing_app.user_id != user_id:
            raise UserNotAuthorizedError(f"User with {user_id} id is not authorized to delete this application")

        await self.app_repo.delete(application_id)
