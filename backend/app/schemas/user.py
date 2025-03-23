# mypy: disable-error-code=assignment
from __future__ import annotations

import re
from datetime import datetime

from pydantic import EmailStr, Field, SecretStr

from .application import ApplicationRead
from .config import Model


class UserRead(Model):
    id: int
    email: EmailStr
    first_name: str | None = Field(max_length=40, default=None)
    second_name: str | None = Field(max_length=40, default=None)
    time_create: datetime
    time_update: datetime
    is_active: bool = True


class UserCreate(Model):
    email: EmailStr
    password: str = Field(
        pattern=re.compile(r"^(?=.*[A-Z])(?=.*\d).{8,}$"),
        description="Password must be 8 characters long, contain at least one uppercase letter and one number.",
    )


class UserUpdate(Model):
    first_name: str | None = Field(max_length=40, default=None)
    second_name: str | None = Field(max_length=40, default=None)
    is_active: bool = True


class UserUpdatePassword(Model):
    password: SecretStr


class UserUpdateEmail(Model):
    email: EmailStr


class UserReadRel(UserRead):
    applications: list["ApplicationRead"]


class UserInDB(Model):
    id: int
    email: EmailStr
    hashed_password: str = Field(alias="password")
    first_name: str | None = Field(max_length=40, default=None)
    second_name: str | None = Field(max_length=40, default=None)
    time_create: datetime
    time_update: datetime
    is_active: bool


class Token(Model):
    access_token: str
    token_type: str


class TokenData(Model):
    username: str | None = None
