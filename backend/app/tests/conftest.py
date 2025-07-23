import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app import env
from app.core.security import IPasswordHasher, ITokenProvider
from app.db import url_object
from app.db.models import Base
from app.dependencies import get_session
from app.infrastructure.security import JWTTokenProvider, PasslibHasher
from app.main import app


@pytest.fixture(scope="session")
def postgres_url():
    return url_object.set(host=env.str("POSTGRES_HOST_TEST")).render_as_string(hide_password=False)


@pytest.fixture(name="session")
async def async_session(postgres_url):
    engine = create_async_engine(postgres_url)
    async_session_maker = async_sessionmaker(engine)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture(autouse=True)
async def override_session_dependency(session):
    app.dependency_overrides[get_session] = lambda: session


@pytest.fixture(autouse=True)
async def cleanup_overrides():
    yield
    app.dependency_overrides = {}


@pytest.fixture(name="client")
async def get_async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
def token_provider() -> ITokenProvider:
    return JWTTokenProvider()


@pytest.fixture(scope="session")
def password_hasher() -> IPasswordHasher:
    return PasslibHasher()
