from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import delete, select, update

from app.core.domain.verification_token import VerificationToken as VerificationTokenDomain
from app.core.repositories.verification_token_repository import IVerificationTokenRepository
from app.db.models import VerificationToken as VerificationTokenModel

from .config import SQLAlchemyRepository


class VerificationTokenSQLAlchemyRepository(SQLAlchemyRepository[VerificationTokenModel], IVerificationTokenRepository):
    model = VerificationTokenModel

    async def create(self, token: VerificationTokenDomain) -> VerificationTokenDomain:
        model = self.model(**token.model_dump(exclude={"id", "used_at", "time_create", "time_update"}))
        self.session.add(model)
        await self.session.flush()
        return VerificationTokenDomain.model_validate(model, from_attributes=True)

    async def get_by_hash(self, token_hash: str) -> VerificationTokenDomain | None:
        statement = select(self.model).where(self.model.token_hash == token_hash)
        model = await self.session.scalar(statement)
        return VerificationTokenDomain.model_validate(model, from_attributes=True) if model else None

    async def delete_all_for_user(self, user_id: int) -> None:
        statement = delete(self.model).where(self.model.user_id == user_id)
        await self.session.execute(statement)

    async def mark_used(self, token_id: int) -> VerificationTokenDomain | None:
        statement = (
            update(self.model)
            .where(self.model.id == token_id)
            .values(used_at=datetime.now(timezone.utc))
            .returning(self.model)
        )
        model = await self.session.scalar(statement)
        return VerificationTokenDomain.model_validate(model, from_attributes=True) if model else None

    async def get_latest_for_user(self, user_id: int) -> VerificationTokenDomain | None:
        statement = (
            select(self.model).where(self.model.user_id == user_id).order_by(self.model.time_create.desc()).limit(1)
        )
        model = await self.session.scalar(statement)
        return VerificationTokenDomain.model_validate(model, from_attributes=True) if model else None
