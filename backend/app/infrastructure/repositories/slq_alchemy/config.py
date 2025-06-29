from __future__ import annotations

from typing import ClassVar, Protocol

from sqlalchemy import exc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions.generic import (
    AlreadyExistError,
    BaseExceptionError,
    NotFoundError,
)
from app.db.models import Base as BaseModel


class SQLAlchemyRepository[T: BaseModel]:
    model: type[T]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _get(
        self, *, limit: int | None = None, offset: int | None = None, **kwargs
    ):
        statement = select(self.model).filter_by(**kwargs).limit(limit).offset(offset)
        return await self.session.scalars(statement)

    async def _get_one(
        self,
        error_message: str | None = None,
        exception_class: type[BaseExceptionError] = NotFoundError,
        **kwargs,
    ):
        items = await self._get(**kwargs)
        try:
            item = items.one()
        except exc.NoResultFound as exp:
            if error_message:
                exception = exception_class(error_message)
            else:
                exception = exception_class()
            raise exception from exp
        return item

    async def _save(
        self,
        model_obj: T,
        error_message: str | None = None,
        exception_class: type[BaseExceptionError] = AlreadyExistError,
    ):
        self.session.add(model_obj)
        try:
            await self.session.flush()
        except exc.IntegrityError as exp:
            if error_message:
                exception = exception_class(error_message)
            else:
                exception = exception_class()
            await self.session.rollback()
            raise exception from exp
        return model_obj


class DataClassProtocol(Protocol):
    __dataclass_fields__: ClassVar[dict]


class SQLAlchemyMapper[T: DataClassProtocol, K: BaseModel]:
    def __init__(self, domain_class: type[T], repo_class: type[K]):
        self.domain = domain_class
        self.repo = repo_class

    def to_domain(self, repo_obj: K) -> T:
        attrs = {k: getattr(repo_obj, k) for k in self.domain.__dataclass_fields__}
        return self.domain(**attrs)

    def to_repo(self, domain_obj: T) -> K:
        return self.repo(**domain_obj.__dict__)
