from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import Field
from typing_extensions import Literal

from app.core.domain import AppStatus, WorkLocation, WorkType

from .company import CompanyCreate, CompanyRead
from .config import BaseModelDTO, GenericFilterParams


class ApplicationRead(BaseModelDTO):
    role: str
    company_id: int
    user_id: int
    id: int
    status: AppStatus
    work_type: WorkType
    work_location: WorkLocation
    note: str | None = None
    application_url: str | None = None
    time_create: datetime
    time_update: datetime
    interview_date: datetime | None = None


class ApplicationReadWithCompany(ApplicationRead):
    company: "CompanyRead"


class ApplicationCreate(BaseModelDTO):
    role: str
    company: "CompanyCreate"
    status: AppStatus = AppStatus.APPLIED
    work_type: WorkType = WorkType.FULL_TIME
    work_location: WorkLocation = WorkLocation.ON_SITE
    note: str | None = None
    application_url: str | None = None
    interview_date: datetime | None = None


class ApplicationUpdate(BaseModelDTO):
    role: str | None = None
    company: "CompanyCreate | None" = None
    status: AppStatus | None = None
    work_type: WorkType | None = None
    work_location: WorkLocation | None = None
    note: str | None = None
    application_url: str | None = None
    interview_date: datetime | None = None


class ApplicationOrderBy(StrEnum):
    time_create = "time_create"
    time_update = "time_update"


class ApplicationFilterParams(GenericFilterParams):
    order_by: ApplicationOrderBy = Field(ApplicationOrderBy.time_create)
    order_direction: Literal["asc", "desc"] = "desc"
