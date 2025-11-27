from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Response, status

from app import Tags
from app.base_schemas import ErrorResponse, MessageResponse
from app.core.dto import UserChangePassword, UserCreate, UserRead, UserResentActivationEmail, UserUpdate
from app.core.exceptions import (
    InactiveUserAlreadyExistError,
    InvalidPasswordError,
    RateLimitExceededError,
    TokenExpireError,
    TokenInvalidError,
    UserAlreadyActivatedError,
    UserAlreadyExistError,
    UserNotFoundError,
)
from app.dependencies import AccessTokenDep, AccessTokenPayloadDep, UserEmailServiceDep, UserServiceDep

from .auth import RefreshTokenSettings

router = APIRouter(prefix="/users", tags=[Tags.USER])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    credentials: Annotated[UserCreate, Form()],
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
        await email_service.send_verification_email(user)
    except UserAlreadyExistError:
        await email_service.send_duplicate_registration_warning(credentials.email)
    except InactiveUserAlreadyExistError:
        user = await user_service.get_by_email(credentials.email)
        await email_service.resend_activation_email(user)

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


@router.post(
    "/resend-activation",
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "User is already activated",
            "model": ErrorResponse,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found (hidden for security)",
            "model": MessageResponse,
        },
        status.HTTP_429_TOO_MANY_REQUESTS: {
            "description": "Too many requests - rate limit exceeded",
            "model": ErrorResponse,
        },
    },
)
async def resend_activation_email(
    form_data: Annotated[UserResentActivationEmail, Form()],
    user_service: UserServiceDep,
    email_service: UserEmailServiceDep,
) -> MessageResponse:
    """
    **Resend** activation email to user.

    This endpoint is rate-limited to prevent abuse. Users must wait a few minutes
    between resend requests. For security reasons, the response doesn't reveal
    whether the email exists in the system.
    """
    try:
        from app import RESEND_ACTIVATION_COOLDOWN_MINUTES

        user = await user_service.resend_activation_email(
            form_data.email, cooldown_minutes=RESEND_ACTIVATION_COOLDOWN_MINUTES
        )
        await email_service.send_verification_email(user)
        return MessageResponse(
            message=f"If an account exists with {form_data.email}, an activation email has been sent"
        )
    except UserAlreadyActivatedError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except RateLimitExceededError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(e),
        ) from e
    except UserNotFoundError:
        return MessageResponse(
            message=f"If an account exists with {form_data.email}, an activation email has been sent"
        )


@router.patch(
    "/change-password",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Old password is incorrect",
            "model": ErrorResponse,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing, invalid, or expired access token",
            "model": ErrorResponse,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
            "model": ErrorResponse,
        },
    },
)
async def change_password(
    access_token: AccessTokenDep, password_form: Annotated[UserChangePassword, Form()], user_service: UserServiceDep
) -> MessageResponse:
    """
    **Change** user password.

    Requires valid access token for authentication.
    """
    try:
        await user_service.change_password_with_token(access_token, password_form)
        return MessageResponse(message="Password changed successfully")
    except (TokenExpireError, TokenInvalidError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid access token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except InvalidPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing, invalid, or expired access token",
            "model": ErrorResponse,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
            "model": ErrorResponse,
        },
    },
)
async def get_current_user(access_token: AccessTokenDep, user_service: UserServiceDep) -> UserRead:
    """
    **Get** current user information.

    Requires valid access token for authentication.
    """
    try:
        user = await user_service.get_by_access_token(access_token)
        return user
    except (TokenExpireError, TokenInvalidError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid access token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.patch(
    "/me",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing, invalid, or expired access token",
            "model": ErrorResponse,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
            "model": ErrorResponse,
        },
    },
)
async def update_user(
    payload: AccessTokenPayloadDep, user_update: UserUpdate, user_service: UserServiceDep
) -> UserRead:
    try:
        user = await user_service.update(payload.user_id, user_update)
    except UserNotFoundError as ex:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(ex)) from ex
    return user


@router.delete(
    "/me",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing, invalid, or expired access token",
            "model": ErrorResponse,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
            "model": ErrorResponse,
        },
    },
)
async def delete_user(
    response: Response, payload: AccessTokenPayloadDep, user_service: UserServiceDep
) -> MessageResponse:
    try:
        await user_service.delete(payload.user_id)
        response.delete_cookie(**asdict(RefreshTokenSettings()))
    except UserNotFoundError as ex:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(ex)) from ex
    return MessageResponse(message="User deleted successfully")
