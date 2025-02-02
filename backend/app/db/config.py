from __future__ import annotations

from decouple import config
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from .models import Base

url_object = URL.create(
    "postgresql+asyncpg",
    config("POSTGRES_USER"),
    config("POSTGRES_PASSWORD"),
    config("POSTGRES_HOST"),
    config("POSTGRES_PORT"),
    config("POSTGRES_DB"),
)

engine = create_async_engine(
    url_object, echo=config("PRINT_SQL_QUERIES", default=False, cast=bool)
)
Session = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_tables(engine: AsyncEngine = engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
