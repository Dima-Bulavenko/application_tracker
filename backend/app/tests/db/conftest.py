# conftest.py
import pytest

from app.db.models import Application, Company, User

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


@pytest.fixture
def new_company():
    return Company(name="test_name")


@pytest.fixture
def new_application(new_company, new_user):
    return Application(
        role="test role",
        company=new_company,
        user=new_user,
        notes="test notes",
        application_url="https://test_url.com",
    )
