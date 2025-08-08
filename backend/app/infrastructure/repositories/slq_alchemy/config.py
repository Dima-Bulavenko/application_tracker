from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Base as BaseModel


class SQLAlchemyRepository[T: BaseModel]:
    model: type[T]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
