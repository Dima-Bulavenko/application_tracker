from __future__ import annotations

from dataclasses import asdict, dataclass

from fastapi import APIRouter, Cookie, Form, HTTPException, Response, status
from typing_extensions import Annotated, Literal

from app import Tags
from app.base_schemas import ErrorResponse
from app.core.dto import AccessTokenResponse, UserLogin
from app.core.exceptions import InvalidPasswordError, TokenExpireError, TokenInvalidError, UserNotFoundError
from app.dependencies import AuthServiceDep, RefreshTokenDep


@dataclass
class RefreshTokenSettings:
    key: str = "refresh"
    path: str = "/auth"
    secure: bool = True
    httponly: bool = True
    samesite: Literal["lax", "strict", "none"] = "none"


router = APIRouter(prefix="/auth", tags=[Tags.AUTHENTICATION])


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
            "model": ErrorResponse,
        },
    },
)
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
    response.set_cookie(**asdict(RefreshTokenSettings()), value=refresh.token, expires=refresh.payload.exp)
    return AccessTokenResponse(access_token=access.token)


@router.post(
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
    response.set_cookie(**asdict(RefreshTokenSettings()), value=refresh.token, expires=refresh.payload.exp)
    return AccessTokenResponse(access_token=access.token)


# FIXME: Review logout logic, because it don't has refresh token rotation, and I need to delete refresh token even if access token is not valid
@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
    response: Response,
    auth_service: AuthServiceDep,
    refresh: Annotated[str | None, Cookie()] = None,
):
    if refresh:
        auth_service.logout(refresh)
    response.delete_cookie(**asdict(RefreshTokenSettings()))
