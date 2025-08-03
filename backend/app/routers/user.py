from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Form, status

from app import Tags
from app.base_schemas import MessageResponse
from app.core.dto import UserCreate
from app.core.exceptions import UserAlreadyExistError
from app.dependencies import UserEmailServiceDep, UserServiceDep

router = APIRouter(prefix="/users", tags=[Tags.USER])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    credentials: Annotated[UserCreate, Form()],
    background_tasks: BackgroundTasks,
    user_service: UserServiceDep,
    email_service: UserEmailServiceDep,
) -> MessageResponse:
    """
    **Create** a user with provided email and password.

    Send link to provided email address for account activation.

    If the user with the email exist, return success response but send warning email to the email address.
    """
    try:
        user = await user_service.create(credentials)
        # Send verification email in background
        background_tasks.add_task(
            email_service.send_verification_email,
            user,
        )
    except UserAlreadyExistError as exp:  #  noqa: F841
        print("user already exist")
        # TODO send user email that someone tried to use his email
        # background_tasks.add_task(
        #     email_service.send_duplicate_registration_warning,
        #     credentials.email
        # )

    return MessageResponse(
        message=f"We sent email to {credentials.email} address, follow link to complete your registration"
    )
