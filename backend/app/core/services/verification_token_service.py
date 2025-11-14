from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta

from app import SECRET_KEY, VERIFICATION_TOKEN_EXPIRE_MINUTES
from app.core.domain import VerificationToken
from app.core.exceptions import TokenExpireError, TokenInvalidError
from app.core.repositories import IVerificationTokenRepository


class VerificationTokenService:
    """Service encapsulating issuance and validation of verification tokens."""

    def __init__(
        self, repo: IVerificationTokenRepository, default_expire_minutes: int = VERIFICATION_TOKEN_EXPIRE_MINUTES
    ) -> None:
        self.repo = repo
        self.default_expire_minutes = default_expire_minutes

    def _hash(self, raw: str) -> str:
        return hmac.new(SECRET_KEY.encode(), raw.encode(), hashlib.sha256).hexdigest()

    async def issue(self, user_id: int, expires_at: datetime | None = None) -> str:
        """Issue a new single-use verification token for a user.

        Deletes existing tokens for that user to prevent multiple valid tokens.
        Returns the raw token value for emailing.
        """
        await self.repo.delete_all_for_user(user_id)
        raw = secrets.token_urlsafe(32)
        expires_at = expires_at or (datetime.now(UTC) + timedelta(minutes=self.default_expire_minutes))
        token_hash = self._hash(raw)
        domain_obj = VerificationToken(user_id=user_id, token_hash=token_hash, expires_at=expires_at)
        await self.repo.create(domain_obj)
        return raw

    async def validate_and_consume(self, raw_token: str) -> int:
        """Validate token; mark used; return user_id.

        Raises TokenInvalidError or TokenExpireError on failure.
        """
        token_hash = self._hash(raw_token)
        token = await self.repo.get_by_hash(token_hash)
        if token is None:
            raise TokenInvalidError("Token is not valid")
        if token.is_used():
            raise TokenInvalidError("Token already used")
        if token.is_expired():
            raise TokenExpireError("Token is expired")
        marked = await self.repo.mark_used(token.id) if token.id is not None else None
        if marked is None:
            raise TokenInvalidError("Token is not valid")
        return token.user_id
