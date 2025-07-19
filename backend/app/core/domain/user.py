from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class User:
    email: str
    password: str
    id: int | None = None
    first_name: str | None = None
    second_name: str | None = None
    time_create: datetime = field(default=datetime.now(UTC))
    time_update: datetime = field(default=datetime.now(UTC))
    is_active: bool = False
