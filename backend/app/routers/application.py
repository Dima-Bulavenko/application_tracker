from fastapi import APIRouter, HTTPException, status

from app import Tags
from app.base_schemas import ErrorResponse
from app.core.dto import ApplicationCreate, ApplicationRead, ApplicationUpdate
from app.core.exceptions import ApplicationNotFoundError, UserNotAuthorizedError
from app.dependencies import ActiveUserDep, ApplicationServiceDep

router = APIRouter(prefix="/applications", tags=[Tags.APPLICATION])


@router.get("/")
async def get_applications_by_email(app_service: ApplicationServiceDep, user: ActiveUserDep) -> list[ApplicationRead]:
    apps = await app_service.get_applications_by_user_email(user.email)
    return apps


@router.post("/")
async def create_application(
    app_service: ApplicationServiceDep, app: ApplicationCreate, user: ActiveUserDep
) -> ApplicationRead:
    application = await app_service.create(app, user.id)
    return application


@router.get(
    "/{application_id}",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Access token is invalid", "model": ErrorResponse},
        status.HTTP_403_FORBIDDEN: {
            "description": "User is not authorized to access this application",
            "model": ErrorResponse,
        },
        status.HTTP_404_NOT_FOUND: {"description": "Application not found", "model": ErrorResponse},
    },
)
async def get_application_by_id(
    application_id: int,
    app_service: ApplicationServiceDep,
    user: ActiveUserDep,
) -> ApplicationRead:
    try:
        application = await app_service.get_by_id(application_id, user.id)
    except ApplicationNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotAuthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    return application


@router.patch(
    "/{application_id}",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Access token is invalid", "model": ErrorResponse},
        status.HTTP_403_FORBIDDEN: {
            "description": "User is not authorized to update this application, or is not active",
            "model": ErrorResponse,
        },
        status.HTTP_404_NOT_FOUND: {"description": "Application or User not found", "model": ErrorResponse},
    },
)
async def update_application(
    application_id: int,
    app_service: ApplicationServiceDep,
    app: ApplicationUpdate,
    user: ActiveUserDep,
) -> ApplicationRead:
    try:
        application = await app_service.update(application_id, app, user.id)
    except ApplicationNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotAuthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    return application


@router.delete(
    "/{application_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Access token is invalid", "model": ErrorResponse},
        status.HTTP_404_NOT_FOUND: {"description": "Application not found", "model": ErrorResponse},
        status.HTTP_403_FORBIDDEN: {
            "description": "User is not authorized to delete this application",
            "model": ErrorResponse,
        },
    },
)
async def delete_application(application_id: int, app_service: ApplicationServiceDep, user: ActiveUserDep) -> None:
    try:
        await app_service.delete(application_id, user.id)
    except ApplicationNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserNotAuthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    return None
