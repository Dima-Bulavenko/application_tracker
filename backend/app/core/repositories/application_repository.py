from __future__ import annotations

from abc import ABC, abstractmethod

from app.core.domain import Application
from app.core.dto import ApplicationFilterParams


class IApplicationRepository(ABC):
    @abstractmethod
    async def create(self, application: Application) -> Application: ...

    @abstractmethod
    async def get_by_user_email(self, email: str, filter_param: ApplicationFilterParams) -> list[Application]: ...

    @abstractmethod
    async def get_by_id(self, application_id: int) -> Application | None: ...

    @abstractmethod
    async def update(self, application_id: int, **update_data) -> Application: ...

    @abstractmethod
    async def delete(self, application_id: int) -> None: ...
