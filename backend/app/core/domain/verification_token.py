from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, Field


class VerificationToken(BaseModel):
    """Domain entity representing an email verification token.

    Stores only a hash of the raw token for security. Single-use enforced by `used_at`.
    """

    user_id: int
    token_hash: str
    expires_at: datetime
    id: int | None = None
    used_at: datetime | None = None
    time_create: datetime = Field(default_factory=lambda: datetime.now(UTC))
    time_update: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def is_expired(self, now: datetime | None = None) -> bool:
        now = now or datetime.now(UTC)
        return now >= self.expires_at

    def is_used(self) -> bool:
        return self.used_at is not None
