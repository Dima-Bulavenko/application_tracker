import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain import User
from app.core.security import IPasswordHasher
from app.db.models import User as UserModel


@pytest.fixture
def user_factory(session: AsyncSession, password_hasher: IPasswordHasher):
    """Factory for creating test users with auto-incremented counter."""
    counter = 0

    async def create_user(**kwargs) -> User:
        """
        Create a test user with auto-incremented counter and valid password.

        Args:
            **kwargs: Additional user attributes to override defaults

        Returns:
            User: Created user domain object
        """
        nonlocal counter
        counter += 1
        params = {
            "email": f"test{counter}@gmail.com",
            "password": f"Test{counter}Pass",
            "is_active": True,
        }

        params.update(kwargs)
        params["password"] = password_hasher.hash(params["password"])

        user = UserModel(**params)

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return User.model_validate(user, from_attributes=True)

    async def create_batch(count: int, **kwargs) -> list[User]:
        """
        Create multiple test users.

        Args:
            count: Number of users to create
            **kwargs: Additional user attributes to override defaults

        Returns:
            list[User]: List of created user domain objects
        """
        return [await create_user(**kwargs) for _ in range(count)]

    create_user.batch = create_batch  # type: ignore[attr-defined]
    return create_user
