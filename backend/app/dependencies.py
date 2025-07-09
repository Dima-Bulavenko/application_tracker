from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dto import AuthTokenPair, AuthTokenPayload, Token, UserLogin, UserRead
from app.core.exceptions import (
    InvalidPasswordError,
    TokenExpireError,
    TokenInvalidError,
    UserNotFoundError,
)
from app.core.services import ApplicationService, AuthService, UserService
from app.infrastructure.repositories import (
    ApplicationSQLAlchemyRepository,
    CompanySQLAlchemyRepository,
    UserSQLAlchemyRepository,
)
from app.infrastructure.security import JWTTokenProvider, PasslibHasher

from .db import Session as SessionMaker


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


async def get_application_service(session: SessionDep) -> ApplicationService:
    return ApplicationService(
        app_repo=ApplicationSQLAlchemyRepository(session),
        user_repo=UserSQLAlchemyRepository(session),
        company_repo=CompanySQLAlchemyRepository(session),
    )


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


def get_refresh_token(refresh: Annotated[str, Cookie()]):
    return Token(token=refresh)


RefreshTokenDep = Annotated[Token, Depends(get_refresh_token)]
LoginUserDep = Annotated[AuthTokenPair, Depends(login_user)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]
LoginFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
ApplicationServiceDep = Annotated[ApplicationService, Depends(get_application_service)]
