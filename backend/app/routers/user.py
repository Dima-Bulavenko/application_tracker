from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Form, HTTPException, status

from app import Tags
from app.base_schemas import ErrorResponse, MessageResponse
from app.core.dto import UserCreate
from app.core.exceptions import (
    TokenExpireError,
    TokenInvalidError,
    UserAlreadyActivatedError,
    UserAlreadyExistError,
    UserNotFoundError,
)
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


@router.patch(
    "/activate",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid or expired activation token",
            "model": ErrorResponse,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
            "model": ErrorResponse,
        },
        status.HTTP_409_CONFLICT: {
            "description": "User is already activated",
            "model": ErrorResponse,
        },
    },
)
async def activate_user(
    token: str,
    user_service: UserServiceDep,
) -> MessageResponse:
    """
    **Activate** user account using verification token.

    Token is typically sent via email during user registration.
    """
    try:
        await user_service.activate_with_token(token)
        return MessageResponse(message="Account activated successfully")
    except (TokenExpireError, TokenInvalidError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid activation token: {str(e)}",
        ) from e
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except UserAlreadyActivatedError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e
