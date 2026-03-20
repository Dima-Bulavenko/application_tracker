import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app import env
from app.core.repositories.user_repository import IUserRepository
from app.core.security import IPasswordHasher
from app.core.services.verification_token_service import VerificationTokenService
from app.db import url_object
from app.db.models import Base
from app.dependencies import get_session
from app.infrastructure.repositories import (
    ApplicationSQLAlchemyRepository,
    CompanySQLAlchemyRepository,
    UserSQLAlchemyRepository,
)
from app.infrastructure.repositories.slq_alchemy.verification_token import VerificationTokenSQLAlchemyRepository
from app.infrastructure.security import (
    AccessTokenStrategy,
    PwdlibHasher,
)
from app.main import app
from app.tests.factories import (
    access_token_factory as access_token_factory,
    application_factory as application_factory,
    company_factory as company_factory,
    refresh_token_factory as refresh_token_factory,
    user_factory as user_factory,
)


@pytest.fixture(scope="session")
def postgres_url():
    return url_object.set(host=env.str("POSTGRES_HOST_TEST"), port=env.int("POSTGRES_PORT_TEST")).render_as_string(
        hide_password=False
    )


@pytest.fixture(name="engine", scope="session")
async def async_engine(postgres_url):
    engine = create_async_engine(postgres_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture(name="session")
async def session_fixture(engine):
    """Provide a session that always rolls back, even if code commits."""
    connection = await engine.connect()
    transaction = await connection.begin()

    async_session_maker = async_sessionmaker(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    async with async_session_maker() as session:
        yield session

    await transaction.rollback()
    await connection.close()


@pytest.fixture(autouse=True)
async def override_session_dependency(session):
    app.dependency_overrides[get_session] = lambda: session
    yield
    app.dependency_overrides.clear()


@pytest.fixture(name="client_config")
def client_config():
    """Provide default client configuration for tests. Can be overridden in individual tests if needed."""
    return {}


@pytest.fixture(name="client")
async def get_async_client(client_config: dict):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
        **client_config,
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
def access_token_strategy() -> AccessTokenStrategy:
    return AccessTokenStrategy()


@pytest.fixture
def verification_token_strategy(session: AsyncSession) -> VerificationTokenService:
    return VerificationTokenService(repo=VerificationTokenSQLAlchemyRepository(session=session))


@pytest.fixture(scope="session")
def password_hasher() -> IPasswordHasher:
    return PwdlibHasher()


@pytest.fixture
def company_repo(session):
    return CompanySQLAlchemyRepository(session)


@pytest.fixture
def application_repo(session):
    return ApplicationSQLAlchemyRepository(session)


@pytest.fixture
def user_repo(session) -> IUserRepository:
    return UserSQLAlchemyRepository(session)
