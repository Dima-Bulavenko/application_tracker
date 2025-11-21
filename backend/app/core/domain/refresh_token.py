from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, Field


class RefreshToken(BaseModel):
    """Domain entity representing a refresh token with revocation and rotation support.

    Stores only a hash of the raw token for security. Supports token families via family_id
    to detect and prevent token reuse attacks.
    """

    user_id: int
    token_hash: str
    family_id: str
    expires_at: datetime
    id: int | None = None
    parent_token_id: int | None = None
    revoked_at: datetime | None = None
    used_at: datetime | None = None
    time_create: datetime = Field(default_factory=lambda: datetime.now(UTC))
    time_update: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def is_expired(self, now: datetime | None = None) -> bool:
        """Check if the token has expired."""
        now = now or datetime.now(UTC)
        return now >= self.expires_at

    def is_revoked(self) -> bool:
        """Check if the token has been explicitly revoked."""
        return self.revoked_at is not None

    def is_used(self) -> bool:
        """Check if the token has been used for rotation."""
        return self.used_at is not None

    def is_valid(self, now: datetime | None = None) -> bool:
        """Check if the token is valid (not expired, revoked, or used)."""
        return not self.is_expired(now) and not self.is_revoked() and not self.is_used()
