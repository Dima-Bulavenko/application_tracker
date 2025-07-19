from __future__ import annotations

import enum
from datetime import UTC, datetime

from pydantic import BaseModel, Field


class AppStatus(enum.Enum):
    APPLIED = "applied"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"


class WorkType(enum.Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    INTERNSHIP = "internship"
    CONTRACT = "contract"
    OTHER = "other"


class WorkLocation(enum.Enum):
    ON_SITE = "on_site"
    REMOTE = "remote"
    HYBRID = "hybrid"


class Application(BaseModel):
    role: str
    company_id: int
    user_id: int
    id: int | None = None
    status: AppStatus = AppStatus.APPLIED
    work_type: WorkType = WorkType.FULL_TIME
    work_location: WorkLocation = WorkLocation.ON_SITE
    notes: str | None = None
    application_url: str | None = None
    time_create: datetime = Field(datetime.now(UTC))
    time_update: datetime = Field(datetime.now(UTC))
    interview_date: datetime | None = None
