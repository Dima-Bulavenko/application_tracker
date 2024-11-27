from __future__ import annotations

from typing import Annotated

from decouple import config
from fastapi import Depends, FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI()

pg_user = config("POSTGRES_USER")
pg_password = config("POSTGRES_PASSWORD")
pg_db_name = config("POSTGRES_DB")
pg_host = config("POSTGRES_HOST")
pg_port = config("POSTGRES_PORT")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db_name}"
)
print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str


sqlite_file_name = "database.db"
sqlite_url = f"postgres///postgres:5432"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
