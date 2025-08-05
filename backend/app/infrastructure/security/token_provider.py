from datetime import datetime, timedelta, timezone

import jwt

from app import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
)
from app.core.dto import (
    AccessTokenPayload,
    BaseModelDTO,
    RefreshTokenPayload,
    Token,
    TokenType,
    VerificationTokenPayload,
)
from app.core.exceptions import TokenExpireError, TokenInvalidError
from app.core.security import ITokenStrategy


class JWTProvider:
    def __init__(self, secret_key: str | None, algorithm: str = ALGORITHM) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create(self, payload: BaseModelDTO) -> str:
        token = jwt.encode(payload.model_dump(), self.secret_key, self.algorithm)
        return token

    def verify(self, token: str) -> dict:
        try:
            dict_payload: dict = jwt.decode(token, self.secret_key, [self.algorithm], options={"require": ["exp"]})
        except jwt.exceptions.ExpiredSignatureError as exp:
            raise TokenExpireError("Token is expired") from exp
        except jwt.exceptions.InvalidTokenError as exp:
            raise TokenInvalidError("Token is not valid") from exp

        return dict_payload


class AccessTokenStrategy(ITokenStrategy[AccessTokenPayload]):
    def __init__(
        self,
        secret_key: str = SECRET_KEY,
        algorithm: str = ALGORITHM,
        expires_in_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES,
    ) -> None:
        self.provider = JWTProvider(secret_key, algorithm)
        self.expires_in_minutes = expires_in_minutes

    def create_token(self, payload: AccessTokenPayload) -> Token[AccessTokenPayload]:
        if payload.exp is None:
            payload.exp = datetime.now(timezone.utc) + timedelta(minutes=self.expires_in_minutes)
        token = self.provider.create(payload)
        return Token(token=token, type=payload.type, payload=payload)

    def verify_token(self, token: str) -> Token[AccessTokenPayload]:
        dict_payload = self.provider.verify(token)
        if dict_payload.get("type") != TokenType.access:
            raise TokenInvalidError("Token is not valid")
        payload = AccessTokenPayload(**dict_payload)
        return Token(token=token, type=payload.type, payload=payload)


class RefreshTokenStrategy(ITokenStrategy[RefreshTokenPayload]):
    def __init__(
        self,
        secret_key: str = SECRET_KEY,
        algorithm: str = ALGORITHM,
        expires_in_minutes: int = REFRESH_TOKEN_EXPIRE_MINUTES,
    ) -> None:
        self.provider = JWTProvider(secret_key, algorithm)
        self.expires_in_minutes = expires_in_minutes

    def create_token(self, payload: RefreshTokenPayload) -> Token[RefreshTokenPayload]:
        if payload.exp is None:
            payload.exp = datetime.now(timezone.utc) + timedelta(minutes=self.expires_in_minutes)
        token = self.provider.create(payload)
        return Token(token=token, type=payload.type, payload=payload)

    def verify_token(self, token: str) -> Token[RefreshTokenPayload]:
        dict_payload = self.provider.verify(token)
        if dict_payload.get("type") != TokenType.refresh:
            raise TokenInvalidError("Token is not valid")
        payload = RefreshTokenPayload(**dict_payload)
        return Token(token=token, type=payload.type, payload=payload)


class VerificationTokenStrategy(ITokenStrategy[VerificationTokenPayload]):
    def __init__(
        self,
        secret_key: str = SECRET_KEY,
        algorithm: str = ALGORITHM,
        expires_in_minutes: int = 10,
    ) -> None:
        self.provider = JWTProvider(secret_key, algorithm)
        self.expires_in_minutes = expires_in_minutes

    def create_token(self, payload: VerificationTokenPayload) -> Token[VerificationTokenPayload]:
        if payload.exp is None:
            payload.exp = datetime.now(timezone.utc) + timedelta(minutes=self.expires_in_minutes)
        token = self.provider.create(payload)
        return Token(token=token, type=payload.type, payload=payload)

    def verify_token(self, token: str) -> Token[VerificationTokenPayload]:
        dict_payload = self.provider.verify(token)
        if dict_payload.get("type") != TokenType.verification:
            raise TokenInvalidError("Token is not valid")
        payload = VerificationTokenPayload(**dict_payload)
        return Token(token=token, type=payload.type, payload=payload)
