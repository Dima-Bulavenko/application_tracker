from __future__ import annotations

from fastapi import APIRouter, Form, HTTPException, Response, status
from typing_extensions import Annotated

from app import Tags
from app.base_schemas import ErrorResponse
from app.core.dto import AccessTokenResponse, RefreshTokenPayload, Token, UserLogin
from app.core.exceptions import InvalidPasswordError, TokenExpireError, TokenInvalidError, UserNotFoundError
from app.dependencies import AccessTokenDep, AuthServiceDep, RefreshTokenDep


def set_refresh_token(response: Response, token: Token[RefreshTokenPayload]) -> None:
    response.set_cookie(
        key="refresh",
        value=token.token,
        expires=token.payload.exp,
        path="auth/refresh",
        secure=True,
        httponly=True,
    )


router = APIRouter(prefix="/auth", tags=[Tags.AUTHENTICATION])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    auth_service: AuthServiceDep, user_data: Annotated[UserLogin, Form()], response: Response
) -> AccessTokenResponse:
    """
    **Create** a user with provided email and password.

    Send link to provided email address for account activation.

    If the user with the email exist, return success response but send warning email to the email address.
    """
    try:
        access, refresh = await auth_service.login_with_credentials(user_data)
    except (UserNotFoundError, InvalidPasswordError) as exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exp
    set_refresh_token(response, refresh)
    return AccessTokenResponse(access_token=access.token)


@router.get(
    "/refresh",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Refresh token is not valid or expired",
            "model": ErrorResponse,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
            "model": ErrorResponse,
        },
    },
)
async def refresh_token(
    auth_service: AuthServiceDep, refresh_token: RefreshTokenDep, response: Response
) -> AccessTokenResponse:
    try:
        access, refresh = await auth_service.refresh_token(refresh_token)
    except (TokenExpireError, TokenInvalidError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    set_refresh_token(response, refresh)
    return AccessTokenResponse(access_token=access.token)


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Access or Refresh token is not valid",
            "model": ErrorResponse,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
            "model": ErrorResponse,
        },
    },
)
async def logout(
    response: Response,
    access_token: AccessTokenDep,
    refresh_token: RefreshTokenDep,
    auth_service: AuthServiceDep,
):
    try:
        await auth_service.logout(access_token, refresh_token)
    except (TokenExpireError, TokenInvalidError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    response.delete_cookie(
        key="refresh",
        path="auth/refresh",
        secure=True,
        httponly=True,
    )
