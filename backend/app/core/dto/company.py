from typing import Annotated

from pydantic import Field

from .config import BaseModelDTO


class CompanyCreate(BaseModelDTO):
    name: Annotated[str, Field(max_length=40)]
