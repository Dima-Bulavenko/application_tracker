from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Annotated

from pydantic import Field
from typing_extensions import Literal

from app.core.domain import AppStatus, WorkLocation, WorkType

from .company import CompanyCreate, CompanyRead
from .config import BaseModelDTO, GenericFilterParams

TRole = Annotated[str, Field(max_length=40)]
TId = Annotated[int, Field(gt=0)]
TStatus = AppStatus
TWorkType = WorkType
TWorkLocation = WorkLocation
TNote = Annotated[str | None, Field(default=None)]
TApplicationUrl = Annotated[str | None, Field(default=None)]
TTimeCreate = datetime
TTimeUpdate = datetime
TInterviewDate = Annotated[datetime | None, Field(default=None)]


class ApplicationRead(BaseModelDTO):
    role: TRole
    company_id: TId
    user_id: TId
    id: TId
    status: TStatus
    work_type: TWorkType
    work_location: TWorkLocation
    note: TNote
    application_url: TApplicationUrl
    time_create: TTimeCreate
    time_update: TTimeUpdate
    interview_date: TInterviewDate


class ApplicationReadWithCompany(ApplicationRead):
    company: "CompanyRead"


class ApplicationCreate(BaseModelDTO):
    role: TRole
    company: "CompanyCreate"
    status: TStatus = AppStatus.APPLIED
    work_type: TWorkType = WorkType.FULL_TIME
    work_location: TWorkLocation = WorkLocation.ON_SITE
    note: TNote
    application_url: TApplicationUrl
    interview_date: TInterviewDate


class ApplicationUpdate(BaseModelDTO):
    role: TRole | None = None
    company: "CompanyCreate | None" = None
    status: TStatus | None = None
    work_type: TWorkType | None = None
    work_location: TWorkLocation | None = None
    note: TNote
    application_url: TApplicationUrl
    interview_date: TInterviewDate


class ApplicationOrderBy(StrEnum):
    time_create = "time_create"
    time_update = "time_update"


class ApplicationFilterParams(GenericFilterParams):
    order_by: ApplicationOrderBy = Field(ApplicationOrderBy.time_create)
    order_direction: Literal["asc", "desc"] = "desc"
    status: list[AppStatus] | None = None
    work_type: list[WorkType] | None = None
    work_location: list[WorkLocation] | None = None
    role_name: str | None = None
    company_name: str | None = None
