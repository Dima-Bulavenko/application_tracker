from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, Field, computed_field


class OAuthProvider(str, Enum):
    LOCAL = "local"
    GOOGLE = "google"
    LINKEDIN = "linkedin"


class User(BaseModel):
    email: str
    password: str | None = None
    oauth_provider: OAuthProvider = OAuthProvider.LOCAL
    oauth_id: str | None = None
    id: int | None = None
    first_name: str | None = None
    second_name: str | None = None
    time_create: datetime = Field(default_factory=lambda: datetime.now(UTC))
    time_update: datetime = Field(default_factory=lambda: datetime.now(UTC))
    is_active: bool = False

    @computed_field  # type: ignore[prop-decorator]
    @property
    def is_password_set(self) -> bool:
        return self.password is not None
