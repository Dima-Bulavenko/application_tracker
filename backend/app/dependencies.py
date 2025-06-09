from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Annotated, cast

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import ALGORITHM, SECRET_KEY
from app.core.dto import AuthTokenPair, UserLogin
from app.core.exceptions import InvalidPasswordError, UserNotFoundError
from app.core.services import AuthService, UserService
from app.db.models.user import User
from app.infrastructure.repositories import UserSQLAlchemyRepository
from app.infrastructure.security import JWTTokenProvider, PasslibHasher
from app.schemas import TokenData
from app.utils import get_user

from .db import Session as SessionMaker

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with SessionMaker() as session:
        yield session
        await session.commit()


async def get_user_service(session: SessionDep) -> UserService:
    return UserService(
        user_repo=UserSQLAlchemyRepository(session), password_hasher=PasslibHasher()
    )


async def get_auth_service(session: SessionDep) -> AuthService:
    return AuthService(
        user_repo=UserSQLAlchemyRepository(session),
        password_hasher=PasslibHasher(),
        token_provider=JWTTokenProvider(),
    )


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
    user = await get_user(session, email=cast("str", token_data.username))
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(user: "CurrentUserDep"):
    if not user.is_active:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return user


async def login_user(
    auth_service: AuthServiceDep, form_data: LoginFormDep
) -> AuthTokenPair:
    try:
        tokens = await auth_service.login_with_credentials(
            UserLogin(email=form_data.username, password=form_data.password)
        )
    except (UserNotFoundError, InvalidPasswordError) as exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exp
    return tokens


LoginUserDep = Annotated[AuthTokenPair, Depends(login_user)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
ActiveCurrentUserDep = Annotated[User, Depends(get_current_active_user)]
LoginFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
