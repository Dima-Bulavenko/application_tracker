import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain import Application
from app.db.models import Application as ApplicationModel


@pytest.fixture
def application_factory(
    session: AsyncSession,
    user_factory,
    company_factory,
):
    """Factory for creating test applications with auto-incremented counter."""
    counter = 0

    async def create_application(
        user_id: int | None = None,
        company_id: int | None = None,
        **kwargs,
    ) -> Application:
        """
        Create a test application with auto-incremented counter.

        Args:
            user_id: User ID, creates new user if None
            company_id: Company ID, creates new company if None
            **kwargs: Additional application attributes to override defaults

        Returns:
            Application: Created application domain object
        """
        nonlocal counter
        counter += 1

        # Create dependencies if not provided
        if company_id is None:
            company = await company_factory()
            company_id = company.id

        if user_id is None:
            user = await user_factory()
            user_id = user.id

        params = {
            "role": f"Test Role {counter}",
            "company_id": company_id,
            "user_id": user_id,
        }

        params.update(kwargs)

        application = ApplicationModel(**params)

        session.add(application)
        await session.commit()
        await session.refresh(application)

        return Application.model_validate(application, from_attributes=True)

    async def create_batch(
        count: int,
        user_id: int | None = None,
        company_id: int | None = None,
        **kwargs,
    ) -> list[Application]:
        """
        Create multiple test applications.

        Args:
            count: Number of applications to create
            user_id: User ID for all applications, creates new user if None
            company_id: Company ID for all applications, creates new company if None
            **kwargs: Additional application attributes to override defaults

        Returns:
            list[Application]: List of created application domain objects
        """
        return [
            await create_application(
                user_id=user_id,
                company_id=company_id,
                **kwargs,
            )
            for _ in range(count)
        ]

    create_application.batch = create_batch  # type: ignore[attr-defined]
    return create_application
