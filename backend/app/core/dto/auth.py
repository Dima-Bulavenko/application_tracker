from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from .config import Model


class TokenType(StrEnum):
    access = "access"
    refresh = "refresh"


class Token(Model):
    token: str
    type: str = "bearer"


class AuthTokenPayload(Model):
    user_email: str
    exp: int | datetime
    type: TokenType


class AuthTokenPair(Model):
    access: Token
    refresh: Token
