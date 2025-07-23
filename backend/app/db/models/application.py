from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.domain import AppStatus, WorkLocation, WorkType

from .config import Base, pk_tp, time_create_tp, time_update_tp
from .user import User


class Application(Base):
    __tablename__ = "application"
    id: Mapped[pk_tp]
    role: Mapped[str] = mapped_column(
        String(40),
        index=True,
    )
    status: Mapped["AppStatus"] = mapped_column(server_default=AppStatus.APPLIED.value)
    company: Mapped["Company"] = relationship(back_populates="applications")
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="applications")
    time_create: Mapped[time_create_tp]
    time_update: Mapped[time_update_tp]
    interview_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    note: Mapped[str | None]
    application_url: Mapped[str | None]
    work_type: Mapped["WorkType"] = mapped_column(index=True, server_default=WorkType.FULL_TIME.value)
    work_location: Mapped["WorkLocation"] = mapped_column(index=True, server_default=WorkLocation.ON_SITE.value)


class Company(Base):
    __tablename__ = "company"
    id: Mapped[pk_tp]
    name: Mapped[str] = mapped_column(String(40), unique=True)
    applications: Mapped[list["Application"]] = relationship(back_populates="company")
