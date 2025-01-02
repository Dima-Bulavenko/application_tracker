# conftest.py
import pytest

from app.db.models import User

from .test_config import SessionLocal, drop_db, init_db


@pytest.fixture
def session():
    init_db()
    session = SessionLocal()
    yield session
    session.close()
    drop_db()


@pytest.fixture
def new_user():
    return User(
        email="test@example.com",
        password="hashedpassword",
        first_name="John",
        second_name="Doe",
        is_active=True,
    )
