from __future__ import annotations

from decouple import config
from models import Base
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

pg_user = config("POSTGRES_USER")
pg_password = config("POSTGRES_PASSWORD")
pg_db_name = config("POSTGRES_DB")
pg_host = config("POSTGRES_HOST")
pg_port = config("POSTGRES_PORT")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
Session = sessionmaker(engine)


def create_db_tables(engine: Engine = engine):
    Base.metadata.create_all(engine)

