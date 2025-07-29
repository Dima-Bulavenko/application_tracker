from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Form, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
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
    return UserService(user_repo=UserSQLAlchemyRepository(session), password_hasher=PasslibHasher())


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


async def login_user(auth_service: AuthServiceDep, user_data: Annotated[UserLogin, Form()]) -> AuthTokenPair:
    try:
        tokens = await auth_service.login_with_credentials(user_data)
    except (UserNotFoundError, InvalidPasswordError) as exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exp
    return tokens


async def get_user(user_service: UserServiceDep, payload: AccessTokenPayloadDep) -> UserRead:
    try:
        user = await user_service.get_by_email(email=payload.user_email)
    except UserNotFoundError as e:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"User with {payload.user_email} email was not found",
        ) from e
    return user


async def get_active_user(user: UserDep) -> UserRead:
    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "User account is not activated")
    return user


def get_refresh_token(request: Request):
    refresh = request.cookies.get("refresh")
    if not refresh:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(token=refresh)


def get_access_token(
    access: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="auth/login"))],
):
    return Token(token=access)


def get_access_token_payload(token: AccessTokenDep):
    exp = HTTPException(status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = JWTTokenProvider().verify_access_token(token)
    except TokenExpireError as e:
        exp.detail = "Token expired"
        raise exp from e
    except TokenInvalidError as e:
        exp.detail = "Token invalid"
        raise exp from e
    return payload


RefreshTokenDep = Annotated[Token, Depends(get_refresh_token)]
AccessTokenDep = Annotated[Token, Depends(get_access_token)]
AccessTokenPayloadDep = Annotated[AuthTokenPayload, Depends(get_access_token_payload)]

UserDep = Annotated[UserRead, Depends(get_user)]
ActiveUserDep = Annotated[UserRead, Depends(get_active_user)]

LoginUserDep = Annotated[AuthTokenPair, Depends(login_user)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
ApplicationServiceDep = Annotated[ApplicationService, Depends(get_application_service)]
