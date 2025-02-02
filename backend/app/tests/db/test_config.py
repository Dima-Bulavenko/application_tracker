# test_config.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import Base

TEST_DATABASE_URL = "sqlite:///:memory:"  # Use an in-memory SQLite database for testing

engine = create_engine(TEST_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def drop_db():
    Base.metadata.drop_all(bind=engine)
