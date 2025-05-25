from passlib.context import CryptContext

from app.core.security import IPasswordHasher


class PasslibHasher(IPasswordHasher):
    def __init__(self) -> None:
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify(self, raw_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(raw_password, hashed_password)
