from datetime import datetime, timedelta, timezone

import jwt

from app import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
)
from app.core.domain import User
from app.core.dto import AuthTokenPayload, TokenType
from app.core.security import ITokenProvider


class JWTTokenProvider(ITokenProvider):
    @staticmethod
    def __create_token(payload: AuthTokenPayload) -> str:
        dict_payload = payload.model_dump()
        token = jwt.encode(dict_payload, SECRET_KEY, ALGORITHM)
        return token

    def create_refresh_token(self, user: User) -> str:
        exp = datetime.now(timezone.utc) + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )
        payload = AuthTokenPayload(
            user_email=user.email, exp=exp, type=TokenType.refresh
        )
        return self.__create_token(payload)

    def create_access_token(self, user: User) -> str:
        exp = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload = AuthTokenPayload(
            user_email=user.email, exp=exp, type=TokenType.access
        )

        return self.__create_token(payload)
