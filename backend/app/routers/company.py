from fastapi import APIRouter

from app import Tags
from app.dependencies import SessionDep
from app.orm import CompanyORM
from app.schemas import CompanyRead

router = APIRouter(prefix="/companies", tags=[Tags.COMPANY])


@router.get("/", response_model=list[CompanyRead])
def get_companies(session: SessionDep):
    return CompanyORM.get_companies(session)
