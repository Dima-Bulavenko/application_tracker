from abc import ABC, abstractmethod

from app.core.domain import User
from app.core.domain.user import OAuthProvider


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None: ...

    @abstractmethod
    async def get_by_oauth_id(self, oauth_provider: OAuthProvider, oauth_id: str) -> User | None:
        """Get user by OAuth provider and OAuth ID"""
        ...

    @abstractmethod
    async def get_by_email_and_provider(self, email: str, oauth_provider: OAuthProvider) -> User | None:
        """Get user by email and OAuth provider"""
        ...

    @abstractmethod
    async def update(self, user_id: int, **update_date) -> User | None: ...

    @abstractmethod
    async def create(self, user: User) -> User: ...

    @abstractmethod
    async def delete(self, user_id: int) -> User | None: ...
