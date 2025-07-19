from __future__ import annotations

import re
from datetime import datetime
from typing import Annotated

from pydantic import EmailStr, Field

from .config import Model as BaseModel

UserPasswordField = Annotated[
    str,
    Field(
        pattern=re.compile(r"^(?=.*[A-Z])(?=.*\d).{8,}$"),
        description="Password must be 8 characters long, contain at least one uppercase letter and one number.",
    ),
]


class UserCreate(BaseModel):
    email: EmailStr
    password: UserPasswordField


class UserRead(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None = Field(max_length=40, default=None)
    second_name: str | None = Field(max_length=40, default=None)
    time_create: datetime
    time_update: datetime
    is_active: bool = True


class UserLogin(BaseModel):
    email: EmailStr
    password: UserPasswordField
