from datetime import datetime, timedelta, timezone
from enum import StrEnum

import jwt

from app import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
)
from app.core.domain import User
from app.core.security import ITokenProvider


class TokenType(StrEnum):
    access = "access"
    refresh = "refresh"


class JWTTokenProvider(ITokenProvider):
    @staticmethod
    def __create_token(payload: dict) -> str:
        token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
        return token

    def create_refresh_token(self, user: User) -> str:
        payload = {
            "email": user.email,
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
            "type": TokenType.refresh,
        }

        return self.__create_token(payload)

    def create_access_token(self, user: User) -> str:
        payload = {
            "email": user.email,
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            "type": TokenType.access,
        }

        return self.__create_token(payload)
