# mypy: disable-error-code=assignment
from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from .config import Model

if TYPE_CHECKING:
    from .application import ApplicationRead


class CompanyBase(Model):
    name: str = Field(min_length=1, max_length=40)


class CompanyRead(CompanyBase):
    id: int


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    name: str | None = Field(min_length=1, max_length=40, default=None)


class CompanyRel(CompanyRead):
    applications: list["ApplicationRead"]
