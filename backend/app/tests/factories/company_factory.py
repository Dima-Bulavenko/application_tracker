import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain import Company
from app.db.models import Company as CompanyModel


@pytest.fixture
def company_factory(session: AsyncSession):
    """Factory for creating test companies with auto-incremented counter."""
    counter = 0

    async def create_company(**kwargs) -> Company:
        """
        Create a test company with auto-incremented counter.

        Args:
            **kwargs: Additional company attributes to override defaults

        Returns:
            Company: Created company domain object
        """
        nonlocal counter
        counter += 1

        params = {
            "name": f"Test Company {counter}",
        }

        params.update(kwargs)

        company = CompanyModel(**params)

        session.add(company)
        await session.commit()
        await session.refresh(company)

        return Company.model_validate(company, from_attributes=True)

    async def create_batch(count: int, **kwargs) -> list[Company]:
        """
        Create multiple test companies.

        Args:
            count: Number of companies to create
            **kwargs: Additional company attributes to override defaults

        Returns:
            list[Company]: List of created company domain objects
        """
        return [await create_company(**kwargs) for _ in range(count)]

    create_company.batch = create_batch  # type: ignore[attr-defined]
    return create_company
