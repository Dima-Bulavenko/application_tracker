from fastapi import APIRouter, Response, status

from app import Tags
from app.core.dto import Token
from app.dependencies import AuthServiceDep, LoginUserDep, RefreshTokenDep
from app.utils import set_refresh_token

router = APIRouter(prefix="/auth", tags=[Tags.AUTHENTICATION])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(tokens: LoginUserDep, response: Response) -> Token:
    """
    **Create** a user with provided email and password.

    Send link to provided email address for account activation.

    If the user with the email exist, return success response but send warning email to the email address.
    """

    set_refresh_token(response, tokens.refresh.token)
    return tokens.access


@router.get("/refresh", status_code=status.HTTP_200_OK)
async def refresh_token(
    auth_service: AuthServiceDep, refresh_token: RefreshTokenDep, response: Response
) -> Token:
    new_tokens = await auth_service.refresh_token(refresh_token)
    set_refresh_token(response, new_tokens.refresh.token)
    return new_tokens.access
