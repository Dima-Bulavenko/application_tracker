import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Company as CompanyModel
from app.infrastructure.repositories import CompanySQLAlchemyRepository


@pytest.fixture(name="repo")
def company_repo(session: AsyncSession):
    return CompanySQLAlchemyRepository(session)


class TestCompanySQLAlchemyRepository:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("res", "params"),
        [
            (6, {}),
            (4, {"limit": 4}),
            (1, {"offset": 5}),
            (2, {"offset": 4, "limit": 4}),
        ],
    )
    async def test_get_companies(
        self, res, params, repo: CompanySQLAlchemyRepository, session: AsyncSession
    ):
        company_names = ["test1", "test2", "test3", "test4", "test5", "test6"]
        session.add_all(CompanyModel(name=n) for n in company_names)
        await session.commit()

        companies = await repo.get_companies(**params)

        assert len(companies) == res
