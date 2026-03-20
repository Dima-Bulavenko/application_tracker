from __future__ import annotations

from sqlalchemy import asc, delete, desc, func, or_, select, update

from app.core.domain import Application
from app.core.dto import ApplicationFilterParams
from app.core.repositories import IApplicationRepository
from app.db.models import Application as ApplicationModel, Company, User

from .config import SQLAlchemyRepository


class ApplicationSQLAlchemyRepository(SQLAlchemyRepository[ApplicationModel], IApplicationRepository):
    model = ApplicationModel

    def _build_filtered_statement(self, email: str, filter_param: ApplicationFilterParams):
        statement = select(self.model).join(User).where(User.email == email)
        if filter_param.role_name:
            statement = statement.where(self.model.role.icontains(filter_param.role_name))

        or_statements = []
        if filter_param.company_name:
            statement = statement.join(Company)
            or_statements.append(Company.name.icontains(filter_param.company_name))
        if filter_param.status:
            or_statements.append(self.model.status.in_(filter_param.status))
        if filter_param.work_type:
            or_statements.append(self.model.work_type.in_(filter_param.work_type))
        if filter_param.work_location:
            or_statements.append(self.model.work_location.in_(filter_param.work_location))
        if or_statements:
            statement = statement.where(or_(*or_statements))
        return statement

    async def create(self, application: Application) -> Application:
        app_model = self.model(**application.model_dump())
        self.session.add(app_model)
        await self.session.flush()
        return Application.model_validate(app_model, from_attributes=True)

    async def get_by_user_email(self, email: str, filter_param: ApplicationFilterParams) -> list[Application]:
        order_by_clause = getattr(self.model, filter_param.order_by)
        order_direction = asc if filter_param.order_direction == "asc" else desc

        statement = self._build_filtered_statement(email, filter_param)

        statement = (
            statement.limit(filter_param.limit).offset(filter_param.offset).order_by(order_direction(order_by_clause))
        )
        apps = await self.session.scalars(statement)
        return [Application.model_validate(app, from_attributes=True) for app in apps]

    async def count_by_user_email(self, email: str, filter_param: ApplicationFilterParams) -> int:
        statement = self._build_filtered_statement(email, filter_param)
        count_statement = select(func.count()).select_from(statement.subquery())
        total = await self.session.scalar(count_statement)
        return total or 0

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
