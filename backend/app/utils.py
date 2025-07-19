from __future__ import annotations

from datetime import datetime, timezone

import jwt
from fastapi import Response
from passlib.context import CryptContext

from app import (
    ALGORITHM,
    SECRET_KEY,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def set_refresh_token(response: Response, token: str) -> None:
    payload = jwt.decode(token, SECRET_KEY, (ALGORITHM,))
    response.set_cookie(
        key="refresh",
        value=token,
        expires=datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc),
        path="auth/refresh",
        secure=True,
        httponly=True,
    )


def delete_refresh_token(response: Response) -> None:
    response.delete_cookie(
        key="refresh",
        path="auth/refresh",
        secure=True,
        httponly=True,
    )
