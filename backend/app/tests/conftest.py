import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app import env
from app.db import url_object
from app.db.models import Base


@pytest.fixture(scope="session")
def postgres_url():
    return url_object.set(host=env.str("POSTGRES_HOST_TEST")).render_as_string(
        hide_password=False
    )


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
