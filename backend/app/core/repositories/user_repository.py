from abc import ABC, abstractmethod

from app.core.domain import User


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> User: ...

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User: ...
