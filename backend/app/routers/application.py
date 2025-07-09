from fastapi import APIRouter

from app import Tags
from app.core.dto import ApplicationCreate, ApplicationRead
from app.dependencies import ActiveUserDep, ApplicationServiceDep

router = APIRouter(prefix="/applications", tags=[Tags.APPLICATION])


@router.get("/")
async def get_applications_by_email(
    app_service: ApplicationServiceDep, user: ActiveUserDep
) -> list[ApplicationRead]:
    apps = await app_service.get_applications_by_user_email(user.email)
    return apps


@router.post("/")
async def create_application(
    app_service: ApplicationServiceDep, app: ApplicationCreate, user: ActiveUserDep
) -> ApplicationRead:
    application = await app_service.create(app, user.id)
    return application
