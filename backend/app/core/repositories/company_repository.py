from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from app.core.domain import Company


class ICompanyRepository(ABC):
    @abstractmethod
    async def create(self, company: Company) -> Company: ...

    @abstractmethod
    async def get_by_name(self, name: str) -> Company | None: ...

    @abstractmethod
    async def get_by_id(self, company_id: int) -> Company | None: ...

    @abstractmethod
    async def get_by_ids(self, company_ids: Iterable[int]) -> list[Company]: ...

    @abstractmethod
    async def get_companies(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Company]: ...
