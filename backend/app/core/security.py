from abc import ABC, abstractmethod

from app.core.domain import User
from app.core.dto import AuthTokenPayload, Token


class IPasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str: ...

    @abstractmethod
    def verify(self, raw_password: str, hashed_password: str) -> bool: ...


class ITokenProvider(ABC):
    @abstractmethod
    def create_access_token(self, user: User) -> Token: ...

    @abstractmethod
    def create_refresh_token(self, user: User) -> Token: ...

    @abstractmethod
    def verify_token(self, token: Token) -> AuthTokenPayload: ...
