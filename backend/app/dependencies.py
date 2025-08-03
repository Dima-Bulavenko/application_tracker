from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dto import AccessTokenPayload, UserRead
from app.core.exceptions import (
    TokenExpireError,
    TokenInvalidError,
    UserNotFoundError,
)
from app.core.services import ApplicationService, AuthService, UserEmailService, UserService
from app.infrastructure.email import DevelopmentEmailService
from app.infrastructure.repositories import (
    ApplicationSQLAlchemyRepository,
    CompanySQLAlchemyRepository,
    UserSQLAlchemyRepository,
)
from app.infrastructure.security import (
    AccessTokenStrategy,
    PasslibHasher,
    RefreshTokenStrategy,
    VerificationTokenStrategy,
)

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
        access_strategy=AccessTokenStrategy(),
        refresh_strategy=RefreshTokenStrategy(),
    )


async def get_application_service(session: SessionDep) -> ApplicationService:
    return ApplicationService(
        app_repo=ApplicationSQLAlchemyRepository(session),
        user_repo=UserSQLAlchemyRepository(session),
        company_repo=CompanySQLAlchemyRepository(session),
    )


async def get_user_email_service() -> UserEmailService:
    return UserEmailService(
        email_service=DevelopmentEmailService(),
        token_handler=VerificationTokenStrategy(),
    )


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


def get_refresh_token(refresh: Annotated[str, Cookie()]) -> str:
    return refresh


def get_access_token(
    access: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="auth/login"))],
) -> str:
    return access


def get_access_token_payload(token: AccessTokenDep) -> AccessTokenPayload:
    exp = HTTPException(status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Bearer"})
    try:
        access = AccessTokenStrategy().verify_token(token)
    except TokenExpireError as e:
        exp.detail = str(e)
        raise exp from e
    except TokenInvalidError as e:
        exp.detail = str(e)
        raise exp from e
    return access.payload


RefreshTokenDep = Annotated[str, Depends(get_refresh_token)]
AccessTokenDep = Annotated[str, Depends(get_access_token)]
AccessTokenPayloadDep = Annotated[AccessTokenPayload, Depends(get_access_token_payload)]

UserDep = Annotated[UserRead, Depends(get_user)]
ActiveUserDep = Annotated[UserRead, Depends(get_active_user)]

SessionDep = Annotated[AsyncSession, Depends(get_session)]

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
ApplicationServiceDep = Annotated[ApplicationService, Depends(get_application_service)]
UserEmailServiceDep = Annotated[UserEmailService, Depends(get_user_email_service)]
