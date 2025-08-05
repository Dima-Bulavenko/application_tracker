from abc import ABC, abstractmethod

from app.core.domain import User


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> User: ...

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User: ...

    @abstractmethod
    async def update(self, user_id: int, **update_date) -> User | None: ...

    @abstractmethod
    async def save(self, user: User) -> User: ...
