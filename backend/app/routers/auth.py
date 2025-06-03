from typing import Annotated

from fastapi import APIRouter, Form, Response, status

from app import Tags
from app.core.dto import Token
from app.dependencies import AuthenticatedUserDep
from app.utils import set_refresh_token

router = APIRouter(prefix="/auth", tags=[Tags.AUTHENTICATION])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(tokens: AuthenticatedUserDep, response: Response) -> Token:
    """
    **Create** a user with provided email and password.

    Send link to provided email address for account activation.

    If the user with the email exist, return success response but send warning email to the email address.
    """
    set_refresh_token(response, tokens.refresh)
    return Token(token=tokens.access)
