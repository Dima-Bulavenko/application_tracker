from __future__ import annotations

from sqlalchemy import select

from app.core.domain import Company
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

    async def get_companies(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Company]:
        statement = select(self.model).limit(limit).offset(offset)
        company_model = await self.session.scalars(statement)
        return [Company.model_validate(c, from_attributes=True) for c in company_model]
