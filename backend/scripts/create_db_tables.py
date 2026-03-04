from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from environs import Env
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


async def main() -> None:
    from app.db.models import Base

    env = Env()
    env.read_env(path=str(ROOT_DIR / ".env"), recurse=False)

    url_object = URL.create(
        "postgresql+asyncpg",
        env.str("POSTGRES_USER"),
        env.str("POSTGRES_PASSWORD"),
        env.str("POSTGRES_HOST"),
        env.int("POSTGRES_PORT"),
        env.str("POSTGRES_DB"),
    )

    engine = create_async_engine(url_object, echo=env.bool("PRINT_SQL_QUERIES", False))

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()


def run() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run()
