from typing import Annotated

from fastapi import APIRouter, Form, status

from app import Tags
from app.base_schemas import MessageResponse
from app.core.dto import UserCreate
from app.core.exceptions import UserAlreadyExistError
from app.dependencies import UserServiceDep

router = APIRouter(prefix="/users", tags=[Tags.USER])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    credentials: Annotated[UserCreate, Form()], service: UserServiceDep
) -> MessageResponse:
    """
    **Create** a user with provided email and password.

    Send link to provided email address for account activation.

    If the user with the email exist, return success response but send warning email to the email address.
    """
    try:
        await service.create(credentials)
    except UserAlreadyExistError as exp:  #  noqa: F841
        print("user already exist")
        # TODO send user email that someone tried to use his email
    # TODO send user activation email
    return MessageResponse(
        message=f"We send email to {credentials.email} address, follow link to complete you registration"
    )
