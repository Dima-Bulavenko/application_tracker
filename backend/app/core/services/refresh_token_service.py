from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta

from app import REFRESH_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from app.core.domain import RefreshToken
from app.core.exceptions import (
    RefreshTokenReuseError,
    RefreshTokenRevokedError,
    TokenExpireError,
    TokenInvalidError,
)
from app.core.repositories import IRefreshTokenRepository


class RefreshTokenService:
    """Service for managing refresh token lifecycle with rotation and revocation.

    Implements strict token rotation and token family tracking to detect and prevent
    token reuse attacks. When a token is rotated, the old token is immediately marked
    as used and invalidated.
    """

    def __init__(
        self,
        repo: IRefreshTokenRepository,
        secret_key: str = SECRET_KEY,
        default_expire_minutes: int = REFRESH_TOKEN_EXPIRE_MINUTES,
    ) -> None:
        self.repo = repo
        self.secret_key = secret_key
        self.default_expire_minutes = default_expire_minutes

    def _hash(self, raw_token: str) -> str:
        """Generate a secure hash of the token for storage."""
        return hmac.new(self.secret_key.encode(), raw_token.encode(), hashlib.sha256).hexdigest()

    def _generate_family_id(self) -> str:
        """Generate a unique family ID for a new token family."""
        return secrets.token_urlsafe(32)

    async def issue(
        self,
        user_id: int,
        family_id: str | None = None,
        parent_token_id: int | None = None,
        expires_at: datetime | None = None,
    ) -> str:
        """Issue a new refresh token for a user.

        Args:
            user_id: The user ID to issue the token for
            family_id: Optional family ID. If None, generates a new family ID (root token)
            parent_token_id: Optional parent token ID for token family tracking
            expires_at: Optional custom expiration time

        Returns:
            The raw token string to be sent to the client
        """
        raw = secrets.token_urlsafe(32)
        expires_at = expires_at or (datetime.now(UTC) + timedelta(minutes=self.default_expire_minutes))
        token_hash = self._hash(raw)

        # Generate new family_id if not provided (root token)
        if family_id is None:
            family_id = self._generate_family_id()

        domain_obj = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            family_id=family_id,
            expires_at=expires_at,
            parent_token_id=parent_token_id,
        )
        await self.repo.create(domain_obj)
        return raw

    async def validate_and_rotate(self, raw_token: str, user_id: int | None = None) -> tuple[str, int]:
        """Validate a refresh token and issue a new one (strict rotation).

        This implements strict token rotation where the old token is immediately
        marked as used. If a used token is presented again, it indicates token
        reuse and the entire token family is revoked.

        Args:
            raw_token: The raw token string from the client
            user_id: Optional expected user ID for additional validation. If provided,
                    validates that the token belongs to this user.

        Returns:
            Tuple of (new raw token string, user_id from the token)

        Raises:
            TokenInvalidError: Token not found or doesn't belong to user (if user_id provided)
            TokenExpireError: Token has expired
            RefreshTokenRevokedError: Token has been revoked
            RefreshTokenReuseError: Token has been used (potential attack)
        """
        token_hash = self._hash(raw_token)
        token = await self.repo.get_by_hash(token_hash)

        if token is None:
            raise TokenInvalidError("Token is not valid")

        if user_id is not None and token.user_id != user_id:
            raise TokenInvalidError("Token does not belong to the specified user")

        # Check if token is expired
        if token.is_expired():
            raise TokenExpireError("Token is expired")

        # Check if token is revoked
        if token.is_revoked():
            raise RefreshTokenRevokedError("Token has been revoked")

        # Check if token has been used - indicates potential reuse attack
        if token.is_used():
            # Security breach detected: token reuse
            # Revoke the entire token family to prevent further abuse
            await self.repo.revoke_token_family(token.family_id)
            raise RefreshTokenReuseError("Token has already been used. Token family revoked for security.")

        # Mark the current token as used
        if token.id is not None:
            await self.repo.mark_used(token.id)

        # Issue a new token with the same family_id and current token as parent
        # Use token.user_id from the validated token
        new_raw_token = await self.issue(token.user_id, family_id=token.family_id, parent_token_id=token.id)
        return new_raw_token, token.user_id

    async def revoke(self, raw_token: str) -> None:
        """Revoke a single refresh token.

        Args:
            raw_token: The raw token string to revoke
        """
        token_hash = self._hash(raw_token)
        token = await self.repo.get_by_hash(token_hash)
        if token and token.id is not None:
            await self.repo.revoke(token.id)

    async def revoke_all_for_user(self, user_id: int) -> None:
        """Revoke all refresh tokens for a user.

        Used when user changes password, logs out from all devices, or is deactivated.

        Args:
            user_id: The user ID whose tokens should be revoked
        """
        await self.repo.revoke_all_for_user(user_id)
