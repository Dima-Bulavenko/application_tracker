from fastapi import APIRouter

from app import Tags
from app.dependencies import ActiveCurrentUserDep, SessionDep
from app.orm import ApplicationORM
from app.schemas import ApplicationCreate, ApplicationReadRel

router = APIRouter(prefix="/applications", tags=[Tags.APPLICATION])


@router.post("/", response_model=ApplicationReadRel)
async def create_application(
    app_data: ApplicationCreate, session: SessionDep, user: ActiveCurrentUserDep
):
    app = await ApplicationORM(session).create(app_data, user)
    session.commit()
    return app


@router.get("/", response_model=list[ApplicationReadRel])
async def get_application(session: SessionDep, user: ActiveCurrentUserDep):
    return await ApplicationORM.get_apps(session)
