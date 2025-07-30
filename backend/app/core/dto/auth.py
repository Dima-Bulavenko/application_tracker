from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from .config import Model


class TokenType(StrEnum):
    access = "access"
    refresh = "refresh"
    verification = "verification"


class Token(Model):
    token: str
    type: TokenType


class AccessTokenPayload(Model):
    user_email: str
    exp: int | datetime
    type: TokenType


class RefreshTokenPayload(Model):
    user_email: str
    exp: int | datetime
    type: TokenType = TokenType.refresh


class VerificationTokenPayload(Model):
    email: str
    exp: int | datetime
    type: TokenType = TokenType.verification


class AccessToken(Token):
    type: TokenType = TokenType.access
    payload: AccessTokenPayload


class RefreshToken(Token):
    type: TokenType = TokenType.refresh
    payload: RefreshTokenPayload


class VerificationToken(Token):
    type: TokenType = TokenType.verification
    payload: VerificationTokenPayload


class AccessTokenResponse(Model):
    access_token: str
    token_type: str = "bearer"
