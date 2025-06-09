from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

import jwt
from fastapi import Response
from passlib.context import CryptContext

from app import (
    ALGORITHM,
    SECRET_KEY,
)
from app.orm import UserORM

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


async def authenticate_user(session: AsyncSession, username: str, password: str):
    user = await get_user(session, email=username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_user(session: AsyncSession, email: str):
    user = await UserORM(session).get(email=email)
    return user


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
