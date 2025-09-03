from fastapi import APIRouter, HTTPException, Query, status
from typing_extensions import Annotated

from app import Tags
from app.base_schemas import ErrorResponse
from app.core.dto import CompanyFilterParams, CompanyRead
from app.core.exceptions import CompanyNotFoundError
from app.dependencies import AccessTokenPayloadDep, CompanyServiceDep

router = APIRouter(prefix="/companies", tags=[Tags.COMPANY])


@router.get(
    "/user",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Access token is invalid", "model": ErrorResponse},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Validation error", "model": ErrorResponse},
    },
)
async def get_user_companies(
    access_token: AccessTokenPayloadDep,
    company_service: CompanyServiceDep,
    filter_param: Annotated[CompanyFilterParams, Query()],
) -> list[CompanyRead]:
    companies = await company_service.get_companies_by_user_id(user_id=access_token.user_id, filter_param=filter_param)
    return companies


@router.get(
    "/{company_id}",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Application not found", "model": ErrorResponse}},
)
async def get_company(company_id: int, company_service: CompanyServiceDep) -> CompanyRead:
    try:
        company = await company_service.get_company_by_id(company_id=company_id)
    except CompanyNotFoundError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))
    return company
