from typing import Annotated

from pydantic import Field

from .config import BaseModelDTO

TName = Annotated[str, Field(max_length=40)]
TId = Annotated[int, Field(gt=0)]


class CompanyCreate(BaseModelDTO):
    name: TName


class CompanyRead(BaseModelDTO):
    id: TId
    name: TName
