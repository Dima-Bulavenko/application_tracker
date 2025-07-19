from fastapi import APIRouter, HTTPException, Response, status

from app import Tags
from app.base_schemas import ErrorResponse
from app.core.dto import AccessToken, Token
from app.core.exceptions import TokenExpireError, TokenInvalidError, UserNotFoundError
from app.dependencies import (
    AccessTokenDep,
    AuthServiceDep,
    LoginUserDep,
    RefreshTokenDep,
)
from app.utils import delete_refresh_token, set_refresh_token

router = APIRouter(prefix="/auth", tags=[Tags.AUTHENTICATION])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(tokens: LoginUserDep, response: Response) -> AccessToken:
    """
    **Create** a user with provided email and password.

    Send link to provided email address for account activation.

    If the user with the email exist, return success response but send warning email to the email address.
    """

    set_refresh_token(response, tokens.refresh.token)
    return AccessToken(access_token=tokens.access.token)


@router.get("/refresh", status_code=status.HTTP_200_OK)
async def refresh_token(
    auth_service: AuthServiceDep, refresh_token: RefreshTokenDep, response: Response
) -> Token:
    new_tokens = await auth_service.refresh_token(refresh_token)
    set_refresh_token(response, new_tokens.refresh.token)
    return new_tokens.access


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
) -> None:
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
    delete_refresh_token(response)
