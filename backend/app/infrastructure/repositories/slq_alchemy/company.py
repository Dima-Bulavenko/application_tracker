from __future__ import annotations

from typing import Iterable

from sqlalchemy import asc, desc, select

from app.core.domain import Company
from app.core.dto import CompanyFilterParams
from app.core.repositories import ICompanyRepository
from app.db.models import Company as CompanyModel

from .config import SQLAlchemyRepository


class CompanySQLAlchemyRepository(SQLAlchemyRepository[CompanyModel], ICompanyRepository):
    model = CompanyModel

    async def create(self, company: Company) -> Company:
        company_model = self.model(**company.model_dump())
        self.session.add(company_model)
        await self.session.flush()
        return Company.model_validate(company_model, from_attributes=True)

    async def get_by_name(self, name: str) -> Company | None:
        statement = select(self.model).where(self.model.name == name)
        company_model = await self.session.scalar(statement)
        return Company.model_validate(company_model, from_attributes=True) if company_model else None

    async def get_by_id(self, company_id: int) -> Company | None:
        statement = select(self.model).where(self.model.id == company_id)
        company_model = await self.session.scalar(statement)
        return Company.model_validate(company_model, from_attributes=True) if company_model else None

    async def get_by_ids(self, company_ids: Iterable[int]) -> list[Company]:
        statement = select(self.model).where(self.model.id.in_(company_ids))
        company_model = await self.session.scalars(statement)
        return [Company.model_validate(c, from_attributes=True) for c in company_model]

    async def get_companies(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Company]:
        statement = select(self.model).limit(limit).offset(offset)
        company_model = await self.session.scalars(statement)
        return [Company.model_validate(c, from_attributes=True) for c in company_model]

    async def get_by_user_id(self, user_id: int, filter_param: CompanyFilterParams) -> list[Company]:
        order_by_clause = getattr(self.model, filter_param.order_by)
        order_direction = asc if filter_param.order_direction == "asc" else desc
        # Start with companies that have at least one application by the user (uses EXISTS via .any)
        statement = select(self.model).where(self.model.applications.any(user_id=user_id))

        # Optional case-insensitive substring filter on name
        if filter_param.name_contains:
            statement = statement.where(self.model.name.icontains(filter_param.name_contains, autoescape=True))

        statement = (
            statement.order_by(order_direction(order_by_clause)).limit(filter_param.limit).offset(filter_param.offset)
        )
        company_model = await self.session.scalars(statement)
        return [Company.model_validate(c, from_attributes=True) for c in company_model]
