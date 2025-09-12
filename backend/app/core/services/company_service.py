from app.core.dto import CompanyFilterParams, CompanyRead
from app.core.exceptions import CompanyNotFoundError
from app.core.repositories import ICompanyRepository


class CompanyService:
    def __init__(self, company_repo: ICompanyRepository):
        self.company_repo = company_repo

    async def get_company_by_id(self, company_id: int) -> CompanyRead:
        company = await self.company_repo.get_by_id(company_id)
        if not company:
            raise CompanyNotFoundError("Company not found")
        return CompanyRead.model_validate(company, from_attributes=True)

    async def get_companies_by_user_id(self, user_id: int, filter_param: CompanyFilterParams) -> list[CompanyRead]:
        companies = await self.company_repo.get_by_user_id(user_id, filter_param)
        return [CompanyRead.model_validate(company, from_attributes=True) for company in companies]
