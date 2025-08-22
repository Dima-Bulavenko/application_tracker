from fastapi import APIRouter, HTTPException, status

from app import Tags
from app.base_schemas import ErrorResponse
from app.core.dto import CompanyRead
from app.core.exceptions import CompanyNotFoundError
from app.dependencies import CompanyServiceDep

router = APIRouter(prefix="/companies", tags=[Tags.COMPANY])


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
