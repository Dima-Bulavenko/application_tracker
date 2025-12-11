from __future__ import annotations

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from app import env
from app.db.models import Base

url_object = URL.create(
    "postgresql+asyncpg",
    env.str("POSTGRES_USER"),
    env.str("POSTGRES_PASSWORD"),
    env.str("POSTGRES_HOST"),
    env.int("POSTGRES_PORT"),
    env.str("POSTGRES_DB"),
)

engine = create_async_engine(url_object, echo=env.bool("PRINT_SQL_QUERIES", False))
Session = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_tables(engine: AsyncEngine = engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
