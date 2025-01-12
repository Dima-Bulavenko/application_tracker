from fastapi import APIRouter

from app import Tags
from app.dependencies import SessionDep
from app.orm import UserORM
from app.schemas import UserCreate, UserRead
from app.utils import get_password_hash

router = APIRouter(prefix="/users", tags=[Tags.USER])


@router.post("/", response_model=UserRead)
async def create_user(credentials: UserCreate, session: SessionDep):
    hashed_password = get_password_hash(credentials.password.get_secret_value())
    user = UserORM.create_user(session, credentials.email, hashed_password)
    session.commit()
    return user
