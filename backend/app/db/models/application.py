from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base, pk_tp, time_create_tp, time_update_tp


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


class Application(Base):
    __tablename__ = "application"
    id: Mapped[pk_tp]
    role: Mapped[str] = mapped_column(String(40), index=True)
    status: Mapped["AppStatus"] = mapped_column(server_default=AppStatus.APPLIED.value)
    company: Mapped["Company"] = relationship(back_populates="applications")
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    time_create: Mapped[time_create_tp]
    time_update: Mapped[time_update_tp]
    interview_date: Mapped[datetime | None]
    notes: Mapped[str | None]
    application_url: Mapped[str | None]
    work_type: Mapped["WorkType"] = mapped_column(
        index=True, server_default=WorkType.FULL_TIME.value
    )
    work_location: Mapped["WorkLocation"] = mapped_column(
        index=True, server_default=WorkLocation.ON_SITE.value
    )


class Company(Base):
    __tablename__ = "company"
    id: Mapped[pk_tp]
    name: Mapped[str] = mapped_column(String(40), unique=True)
    applications: Mapped[list["Application"]] = relationship(back_populates="company")
    location: Mapped[str]
