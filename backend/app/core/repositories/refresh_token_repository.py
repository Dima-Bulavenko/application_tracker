from __future__ import annotations

from abc import ABC, abstractmethod

from app.core.domain import RefreshToken


class IRefreshTokenRepository(ABC):
    """Repository interface for refresh tokens with rotation and revocation support."""

    @abstractmethod
    async def create(self, token: RefreshToken) -> RefreshToken:
        """Create a new refresh token in the database."""
        ...

    @abstractmethod
    async def get_by_hash(self, token_hash: str) -> RefreshToken | None:
        """Retrieve a refresh token by its hash."""
        ...

    @abstractmethod
    async def get_by_id(self, token_id: int) -> RefreshToken | None:
        """Retrieve a refresh token by its ID."""
        ...

    @abstractmethod
    async def mark_used(self, token_id: int) -> RefreshToken | None:
        """Mark a token as used (for rotation)."""
        ...

    @abstractmethod
    async def revoke(self, token_id: int) -> RefreshToken | None:
        """Revoke a single token by ID."""
        ...

    @abstractmethod
    async def revoke_token_family(self, family_id: str) -> None:
        """Revoke an entire token family by family_id.

        This is used when token reuse is detected - all tokens in the family
        should be revoked to prevent further abuse.
        """
        ...

    @abstractmethod
    async def revoke_all_for_user(self, user_id: int) -> None:
        """Revoke all tokens for a specific user.

        Used when user changes password, logs out from all devices, or is deactivated.
        """
        ...
