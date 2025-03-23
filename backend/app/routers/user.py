from typing import Annotated

from fastapi import APIRouter, Form

from app import Tags
from app.dependencies import SessionDep
from app.orm import UserORM
from app.schemas import UserCreate, UserRead
from app.utils import get_password_hash

router = APIRouter(prefix="/users", tags=[Tags.USER])


@router.post("/", response_model=UserRead)
async def create_user(credentials: Annotated[UserCreate, Form()], session: SessionDep):
    hashed_password = get_password_hash(credentials.password)
    user = await UserORM(session).create(credentials.email, hashed_password)
    return user
