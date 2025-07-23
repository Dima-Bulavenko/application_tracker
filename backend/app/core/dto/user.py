from __future__ import annotations

import re
from datetime import datetime
from typing import Annotated

from pydantic import AliasChoices, EmailStr, Field

from .config import Model as BaseModel

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


class UserCreate(BaseModel):
    email: UserEmailField
    password: UserPasswordField


class UserRead(BaseModel):
    id: int
    email: UserEmailField
    first_name: str | None = Field(max_length=40, default=None)
    second_name: str | None = Field(max_length=40, default=None)
    time_create: datetime
    time_update: datetime
    is_active: bool = True


class UserLogin(BaseModel):
    email: UserEmailField
    password: UserPasswordField
