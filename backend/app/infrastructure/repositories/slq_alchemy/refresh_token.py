from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select, update

from app.core.domain.refresh_token import RefreshToken as RefreshTokenDomain
from app.core.repositories.refresh_token_repository import IRefreshTokenRepository
from app.db.models import RefreshToken as RefreshTokenModel

from .config import SQLAlchemyRepository


class RefreshTokenSQLAlchemyRepository(SQLAlchemyRepository[RefreshTokenModel], IRefreshTokenRepository):
    model = RefreshTokenModel

    async def create(self, token: RefreshTokenDomain) -> RefreshTokenDomain:
        model = self.model(**token.model_dump(exclude={"id", "revoked_at", "used_at", "time_create", "time_update"}))
        self.session.add(model)
        await self.session.flush()
        return RefreshTokenDomain.model_validate(model, from_attributes=True)

    async def get_by_hash(self, token_hash: str) -> RefreshTokenDomain | None:
        statement = select(self.model).where(self.model.token_hash == token_hash)
        model = await self.session.scalar(statement)
        return RefreshTokenDomain.model_validate(model, from_attributes=True) if model else None

    async def get_by_id(self, token_id: int) -> RefreshTokenDomain | None:
        statement = select(self.model).where(self.model.id == token_id)
        model = await self.session.scalar(statement)
        return RefreshTokenDomain.model_validate(model, from_attributes=True) if model else None

    async def mark_used(self, token_id: int) -> RefreshTokenDomain | None:
        statement = (
            update(self.model)
            .where(self.model.id == token_id)
            .values(used_at=datetime.now(timezone.utc))
            .returning(self.model)
        )
        model = await self.session.scalar(statement)
        return RefreshTokenDomain.model_validate(model, from_attributes=True) if model else None

    async def revoke(self, token_id: int) -> RefreshTokenDomain | None:
        statement = (
            update(self.model)
            .where(self.model.id == token_id)
            .values(revoked_at=datetime.now(timezone.utc))
            .returning(self.model)
        )
        model = await self.session.scalar(statement)
        return RefreshTokenDomain.model_validate(model, from_attributes=True) if model else None

    async def revoke_token_family(self, family_id: str) -> None:
        """Revoke entire token family by family_id.

        This handles token reuse detection by revoking all tokens
        that belong to the same family.
        """
        statement = (
            update(self.model).where(self.model.family_id == family_id).values(revoked_at=datetime.now(timezone.utc))
        )
        await self.session.execute(statement)

    async def revoke_all_for_user(self, user_id: int) -> None:
        statement = (
            update(self.model).where(self.model.user_id == user_id).values(revoked_at=datetime.now(timezone.utc))
        )
        await self.session.execute(statement)
