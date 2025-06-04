from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from .config import Model


class TokenType(StrEnum):
    access = "access"
    refresh = "refresh"


class Tokens(Model):
    access: str
    refresh: str


class Token(Model):
    token: str
    type: str = "bearer"


class AuthTokenPayload(Model):
    user_email: str
    exp: int | datetime
    type: TokenType
