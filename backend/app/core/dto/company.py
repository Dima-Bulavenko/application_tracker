from typing import Annotated

from pydantic import Field

from .config import Model


class CompanyCreate(Model):
    name: Annotated[str, Field(max_length=40)]
