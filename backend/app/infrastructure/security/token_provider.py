from datetime import datetime, timedelta, timezone

import jwt

from app import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
)
from app.core.domain import User
from app.core.dto import (
    AccessToken,
    AccessTokenPayload,
    BaseModelDTO,
    RefreshToken,
    RefreshTokenPayload,
    TokenType,
    VerificationToken,
    VerificationTokenPayload,
)
from app.core.exceptions import TokenExpireError, TokenInvalidError
from app.core.security import ITokenProvider


class JWTTokenProvider(ITokenProvider):
    @staticmethod
    def __create_token(payload: BaseModelDTO) -> str:
        token = jwt.encode(payload.model_dump(), SECRET_KEY, ALGORITHM)
        return token

    def __verify(self, token: str, token_type: TokenType) -> dict:
        try:
            dict_payload: dict = jwt.decode(token, SECRET_KEY, [ALGORITHM], options={"require": ["exp"]})
        except jwt.exceptions.ExpiredSignatureError as exp:
            raise TokenExpireError("Token is expired") from exp
        except jwt.exceptions.InvalidTokenError as exp:
            raise TokenInvalidError("Token is not valid") from exp

        if dict_payload.get("type") != token_type:
            raise TokenInvalidError("Token is not valid")

        return dict_payload

    def create_refresh_token(self, user: User) -> RefreshToken:
        exp = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        payload = RefreshTokenPayload(user_email=user.email, exp=exp, type=TokenType.refresh)

        return RefreshToken(token=self.__create_token(payload), payload=payload)

    def create_access_token(self, user: User) -> AccessToken:
        exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = AccessTokenPayload(user_email=user.email, exp=exp, type=TokenType.access)

        return AccessToken(token=self.__create_token(payload), payload=payload)

    def create_verification_token(self, user_email: str) -> VerificationToken:
        exp = datetime.now(timezone.utc) + timedelta(hours=24)  # 24 hours expiration
        payload = VerificationTokenPayload(email=user_email, exp=exp, type=TokenType.verification)

        return VerificationToken(token=self.__create_token(payload), payload=payload)

    def verify_refresh_token(self, token: str) -> RefreshToken:
        token_payload = self.__verify(token, TokenType.refresh)
        return RefreshToken(token=token, payload=RefreshTokenPayload(**token_payload))

    def verify_access_token(self, token: str) -> AccessToken:
        token_payload = self.__verify(token, TokenType.access)
        return AccessToken(token=token, payload=AccessTokenPayload(**token_payload))

    def verify_verification_token(self, token: str) -> VerificationToken:
        token_payload = self.__verify(token, TokenType.access)
        return VerificationToken(token=token, payload=VerificationTokenPayload(**token_payload))
