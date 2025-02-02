# test_user.py
import pytest
from sqlalchemy.exc import IntegrityError

from app.db.models import User


def test_create_user(session, new_user):
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    assert new_user.id is not None
    assert new_user.email == "test@example.com"
    assert new_user.first_name == "John"
    assert new_user.second_name == "Doe"
    assert new_user.is_active is True


def test_unique_email_constraint(session, new_user):
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    duplicate_user = User(
        email="test@example.com",
        password="anotherpassword",
        first_name="Jane",
        second_name="Smith",
        is_active=True,
    )
    session.add(duplicate_user)
    error_msg = "UNIQUE constraint failed: user.email"
    with pytest.raises(IntegrityError, match=error_msg):
        session.commit()


def test_default_is_active(session, new_user):
    new_user.is_active = None
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    assert new_user.is_active is True
