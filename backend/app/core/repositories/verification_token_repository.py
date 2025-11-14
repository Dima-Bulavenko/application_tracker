from __future__ import annotations

from abc import ABC, abstractmethod

from app.core.domain import VerificationToken


class IVerificationTokenRepository(ABC):
    """Repository interface for verification tokens."""

    @abstractmethod
    async def create(self, token: VerificationToken) -> VerificationToken: ...

    @abstractmethod
    async def get_by_hash(self, token_hash: str) -> VerificationToken | None: ...

    @abstractmethod
    async def delete_all_for_user(self, user_id: int) -> None: ...

    @abstractmethod
    async def mark_used(self, token_id: int) -> VerificationToken | None: ...
