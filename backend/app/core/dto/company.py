from enum import StrEnum
from typing import Annotated, Literal

from pydantic import Field

from .config import BaseModelDTO, GenericFilterParams

TName = Annotated[str, Field(max_length=40)]
TId = Annotated[int, Field(gt=0)]


class CompanyCreate(BaseModelDTO):
    name: TName


class CompanyRead(BaseModelDTO):
    id: TId
    name: TName


class CompanyOrderBy(StrEnum):
    company_name = "name"


class CompanyFilterParams(GenericFilterParams):
    order_by: CompanyOrderBy = CompanyOrderBy.company_name
    order_direction: Literal["asc", "desc"] = "desc"
    name_contains: str | None = None
