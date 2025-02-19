from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Annotated, cast

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import ALGORITHM, SECRET_KEY
from app.db.models.user import User
from app.schemas import TokenData
from app.utils import get_user, verify_password

from .db import Session as SessionMaker

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with SessionMaker() as session:
        yield session
        await session.commit()


async def get_current_user(token: "TokenDep", session: "SessionDep"):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception from None
    user = await get_user(session, email=cast(str, token_data.username))
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(user: "CurrentUserDep"):
    if not user.is_active:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return user


async def authenticate_user(session: SessionDep, form_data: LoginFormDep):
    invalid_credentials = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = await get_user(session, email=form_data.username)
    if not user:
        raise invalid_credentials
    if not verify_password(form_data.password, user.password):
        raise invalid_credentials
    return user


AuthenticatedUserDep = Annotated[User, Depends(authenticate_user)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
ActiveCurrentUserDep = Annotated[User, Depends(get_current_active_user)]
LoginFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
