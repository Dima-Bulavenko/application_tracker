# mypy: disable-error-code=assignment
from __future__ import annotations

from datetime import datetime

from pydantic import Field, HttpUrl

from app.db.models import AppStatus, WorkLocation, WorkType

from .company import CompanyCreate, CompanyRead
from .config import Model


class ApplicationBase(Model):
    role: str = Field(max_length=40)
    work_type: "WorkType" = WorkType.FULL_TIME
    work_location: "WorkLocation" = WorkLocation.ON_SITE
    application_url: HttpUrl | None = None
    notes: str | None = Field(max_length=2000, default=None)
    interview_date: datetime | None = None


class ApplicationCreate(ApplicationBase):
    company: "CompanyCreate"


class ApplicationRead(ApplicationBase):
    id: int
    status: "AppStatus" = AppStatus.APPLIED
    time_create: datetime
    time_update: datetime


class ApplicationUpdate(ApplicationBase):
    role: str | None = Field(min_length=1, max_length=40, default=None)
    status: "AppStatus | None" = None
    work_type: "WorkType | None" = None
    work_location: "WorkLocation | None" = None
    notes: str | None = None
    application_url: HttpUrl | None = None
    company: "CompanyRead | None" = None
    interview_date: datetime | None = None


class ApplicationReadRel(ApplicationRead):
    company: "CompanyRead"
