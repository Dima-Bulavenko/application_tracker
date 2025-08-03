import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain import Application, Company, User
from app.core.dto import AccessTokenPayload, RefreshTokenPayload, Token
from app.core.security import IPasswordHasher, ITokenStrategy
from app.db.models import Application as ApplicationModel
from app.db.models import Company as CompanyModel
from app.db.models import User as UserModel


class BaseTest:
    """Base test class providing common testing utilities and setup."""

    @pytest.fixture(autouse=True)
    def setup(
        self,
        session: AsyncSession,
        password_hasher: IPasswordHasher,
        access_token_strategy: ITokenStrategy[AccessTokenPayload],
        refresh_token_strategy: ITokenStrategy[RefreshTokenPayload],
    ):
        """Set up common test dependencies and counters."""
        self.session = session
        self.access_token_strategy = access_token_strategy
        self.refresh_token_strategy = refresh_token_strategy
        self.password_hasher = password_hasher

        # Initialize counters for unique test data
        self.user_counter = 0
        self.company_counter = 0
        self.application_counter = 0
        yield
        # Reset counters after each test
        self.user_counter = 0
        self.company_counter = 0
        self.application_counter = 0

    async def create_user(self, **kwargs) -> User:
        """
        Create a test user with auto-incremented counter and valid password.

        Args:
            **kwargs: Additional user attributes to override defaults

        Returns:
            User: Created user domain object
        """
        self.user_counter += 1
        password = f"Test{self.user_counter}Pass"  # Valid password: uppercase, digit, 8+ chars

        user_data = {
            "email": f"test{self.user_counter}@gmail.com",
            "password": self.password_hasher.hash(password),
            "is_active": True,  # Default to active user
            **kwargs,
        }

        user = UserModel(**user_data)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return User(**{f: getattr(user, f) for f in User.__dataclass_fields__})

    async def create_company(self, **kwargs) -> Company:
        """
        Create a test company with auto-incremented counter.

        Args:
            **kwargs: Additional company attributes to override defaults

        Returns:
            Company: Created company domain object
        """
        self.company_counter += 1
        company_data = {
            "name": f"Test Company {self.company_counter}",
            **kwargs,
        }

        company = CompanyModel(**company_data)
        self.session.add(company)
        await self.session.commit()
        await self.session.refresh(company)
        return Company.model_validate(company, from_attributes=True)

    async def create_application(
        self, user_id: int | None = None, company_id: int | None = None, **kwargs
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
        self.application_counter += 1

        # Create dependencies if not provided
        if company_id is None:
            company = await self.create_company()
            company_id = company.id

        if user_id is None:
            user = await self.create_user()
            user_id = user.id

        application_data = {
            "role": f"Test Role {self.application_counter}",
            "company_id": company_id,
            "user_id": user_id,
            **kwargs,
        }

        application = ApplicationModel(**application_data)
        self.session.add(application)
        await self.session.commit()
        await self.session.refresh(application)
        return Application.model_validate(application, from_attributes=True)

    def get_user_password(self, user_number: int | None = None) -> str:
        """
        Get the password for a specific user or the most recently created user.

        Args:
            user_number: Specific user number, defaults to current counter

        Returns:
            str: The password for the user
        """
        if user_number is None:
            user_number = self.user_counter
        return f"Test{user_number}Pass"

    async def get_application(self, app_id: int) -> ApplicationModel | None:
        statement = select(ApplicationModel).where(ApplicationModel.id == app_id)
        app = await self.session.scalar(statement)
        return app

    async def get_company(self, company_id: int) -> CompanyModel | None:
        statement = select(CompanyModel).where(CompanyModel.id == company_id)
        company = await self.session.scalar(statement)
        return company

    def create_access_token(self, user: User) -> Token[AccessTokenPayload]:
        assert user.id is not None, "User ID must be set to create access token"
        payload = AccessTokenPayload(user_email=user.email, user_id=user.id)
        return self.access_token_strategy.create_token(payload)

    def create_refresh_token(self, user: User) -> Token[RefreshTokenPayload]:
        assert user.id is not None, "User ID must be set to create refresh token"
        payload = RefreshTokenPayload(user_email=user.email, user_id=user.id)
        return self.refresh_token_strategy.create_token(payload)
