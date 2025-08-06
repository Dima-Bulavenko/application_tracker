from __future__ import annotations

import re
from datetime import datetime
from typing import Annotated

from pydantic import AliasChoices, EmailStr, Field, ValidationInfo, field_validator

from .config import BaseModelDTO

UserPasswordField = Annotated[
    str,
    Field(
        pattern=re.compile(r"^(?=.*[A-Z])(?=.*\d).{8,}$"),
        description="Password must be 8 characters long, contain at least one uppercase letter and one number.",
    ),
]

UserEmailField = Annotated[
    EmailStr,
    Field(
        validation_alias=AliasChoices("username", "email"),
        serialization_alias="username",
        description="User's email address",
    ),
]


class UserCreate(BaseModelDTO):
    email: UserEmailField
    password: UserPasswordField


class UserRead(BaseModelDTO):
    id: int
    email: UserEmailField
    first_name: str | None = Field(max_length=40, default=None)
    second_name: str | None = Field(max_length=40, default=None)
    time_create: datetime
    time_update: datetime
    is_active: bool = True


class UserLogin(BaseModelDTO):
    email: UserEmailField
    password: UserPasswordField


class UserChangePassword(BaseModelDTO):
    old_password: UserPasswordField
    new_password: UserPasswordField
    confirm_new_password: UserPasswordField

    @field_validator("confirm_new_password", mode="after")
    @classmethod
    def validate_confirm_password(cls, value: str, info: ValidationInfo) -> str:
        if value != info.data.get("new_password"):
            raise ValueError("New password and confirmation do not match")
        return value
