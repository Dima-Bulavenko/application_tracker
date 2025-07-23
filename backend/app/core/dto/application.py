from __future__ import annotations

from datetime import UTC, datetime

from pydantic import Field

from app.core.domain import AppStatus, WorkLocation, WorkType

from .company import CompanyCreate
from .config import Model


class ApplicationRead(Model):
    role: str
    company_id: int
    user_id: int
    id: int
    status: AppStatus = AppStatus.APPLIED
    work_type: WorkType = WorkType.FULL_TIME
    work_location: WorkLocation = WorkLocation.ON_SITE
    note: str | None = None
    application_url: str | None = None
    time_create: datetime = Field(datetime.now(UTC))
    time_update: datetime = Field(datetime.now(UTC))
    interview_date: datetime | None = None


class ApplicationCreate(Model):
    role: str
    company: "CompanyCreate"
    status: AppStatus = AppStatus.APPLIED
    work_type: WorkType = WorkType.FULL_TIME
    work_location: WorkLocation = WorkLocation.ON_SITE
    note: str | None = None
    application_url: str | None = None
    time_create: datetime = Field(datetime.now(UTC))
    time_update: datetime = Field(datetime.now(UTC))
    interview_date: datetime | None = None


class ApplicationUpdate(Model):
    role: str | None = None
    company: "CompanyCreate | None" = None
    status: AppStatus | None = None
    work_type: WorkType | None = None
    work_location: WorkLocation | None = None
    note: str | None = None
    application_url: str | None = None
    interview_date: datetime | None = None
