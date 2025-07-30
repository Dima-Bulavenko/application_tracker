from abc import ABC, abstractmethod

from app.core.domain import User
from app.core.dto import AccessToken, RefreshToken, VerificationToken


class IPasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str: ...

    @abstractmethod
    def verify(self, raw_password: str, hashed_password: str) -> bool: ...


class ITokenProvider(ABC):
    @abstractmethod
    def create_access_token(self, user: User) -> AccessToken: ...

    @abstractmethod
    def create_refresh_token(self, user: User) -> RefreshToken: ...

    @abstractmethod
    def verify_refresh_token(self, token: str) -> RefreshToken: ...

    @abstractmethod
    def verify_access_token(self, token: str) -> AccessToken: ...

    @abstractmethod
    def create_verification_token(self, user_email: str) -> VerificationToken: ...

    @abstractmethod
    def verify_verification_token(self, token: str) -> VerificationToken: ...
