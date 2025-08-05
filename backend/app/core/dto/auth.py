from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Literal

from .config import BaseModelDTO


class TokenType(StrEnum):
    access = "access"
    refresh = "refresh"
    verification = "verification"


class Token[PayloadT: BaseModelDTO](BaseModelDTO):
    token: str
    type: TokenType
    payload: PayloadT


class AccessTokenPayload(BaseModelDTO):
    user_email: str
    user_id: int
    exp: datetime | None = None
    type: Literal[TokenType.access] = TokenType.access


class RefreshTokenPayload(BaseModelDTO):
    user_email: str
    user_id: int
    exp: datetime | None = None
    type: Literal[TokenType.refresh] = TokenType.refresh


class VerificationTokenPayload(BaseModelDTO):
    user_email: str
    user_id: int
    exp: datetime | None = None
    type: Literal[TokenType.verification] = TokenType.verification


class AccessTokenResponse(BaseModelDTO):
    access_token: str
    token_type: str = "bearer"
