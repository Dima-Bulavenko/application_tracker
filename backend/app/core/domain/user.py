from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, Field


class User(BaseModel):
    email: str
    password: str
    id: int | None = None
    first_name: str | None = None
    second_name: str | None = None
    time_create: datetime = Field(default_factory=lambda: datetime.now(UTC))
    time_update: datetime = Field(default_factory=lambda: datetime.now(UTC))
    is_active: bool = False
