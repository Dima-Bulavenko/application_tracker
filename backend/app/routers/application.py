from fastapi import APIRouter

from app import Tags
from app.dependencies import ActiveCurrentUserDep, SessionDep
from app.orm import ApplicationORM
from app.schemas import ApplicationCreate, ApplicationReadRel

router = APIRouter(prefix="/applications", tags=[Tags.APPLICATION])


@router.post("/", response_model=ApplicationReadRel)
async def create_application(
    new_app: ApplicationCreate, session: SessionDep, user: ActiveCurrentUserDep
):
    app = await ApplicationORM.create_app(new_app, session, user)
    session.commit()
    return app


@router.get("/", response_model=list[ApplicationReadRel])
async def get_application(session: SessionDep, user: ActiveCurrentUserDep):
    return await ApplicationORM.get_apps(session)
