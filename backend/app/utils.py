from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

import jwt
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


def create_token(payload: dict, expires_delta: timedelta | int):
    if isinstance(expires_delta, int):
        expires_delta = timedelta(minutes=expires_delta)
    to_encode = payload.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_user(session: AsyncSession, email: str):
    user = await UserORM(session).get(email=email)
    return user
