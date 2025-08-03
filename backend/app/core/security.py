from abc import ABC, abstractmethod

from app.core.dto import BaseModelDTO, Token


class IPasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str: ...

    @abstractmethod
    def verify(self, raw_password: str, hashed_password: str) -> bool: ...


class ITokenStrategy[PayloadT: BaseModelDTO](ABC):
    @abstractmethod
    def create_token(self, payload: PayloadT) -> Token[PayloadT]: ...

    @abstractmethod
    def verify_token(self, token: str) -> Token[PayloadT]: ...
