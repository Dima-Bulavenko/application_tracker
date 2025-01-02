from __future__ import annotations

from decouple import config
from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

url_object = URL.create(
    "postgresql",
    config("POSTGRES_USER"),
    config("POSTGRES_PASSWORD"),
    config("POSTGRES_HOST"),
    config("POSTGRES_PORT"),
    config("POSTGRES_DB"),
)

engine = create_engine(
    url_object, echo=config("PRINT_SQL_QUERIES", default=False, cast=bool)
)
Session = sessionmaker(engine)


def create_db_tables(engine: Engine = engine):
    Base.metadata.create_all(engine)
