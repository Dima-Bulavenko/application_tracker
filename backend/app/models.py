from __future__ import annotations

import enum
from datetime import datetime

import sqlalchemy as sq
from decouple import config
from sqlalchemy import DateTime, Engine, ForeignKey, String, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

pg_user = config("POSTGRES_USER")
pg_password = config("POSTGRES_PASSWORD")
pg_db_name = config("POSTGRES_DB")
pg_host = config("POSTGRES_HOST")
pg_port = config("POSTGRES_PORT")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)


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


class Base(DeclarativeBase):
    type_annotation_map = {
        enum.Enum: sq.Enum(values_callable=lambda x: [e.value for e in x])
    }


class Application(Base):
    __tablename__ = "application"
    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(String(40), index=True)
    status: Mapped[AppStatus] = mapped_column(server_default=AppStatus.APPLIED.value)
    company: Mapped[Company] = relationship(back_populates="applications")
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    time_create: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    time_update: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
    interview_date: Mapped[datetime | None]
    notes: Mapped[str | None]
    application_url: Mapped[str | None]
    work_type: Mapped[WorkType] = mapped_column(index=True, server_default=WorkType.FULL_TIME.value)
    work_location: Mapped[WorkLocation] = mapped_column(index=True, server_default=WorkLocation.ON_SITE.value)


class Company(Base):
    __tablename__ = "company"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), unique=True)
    applications: Mapped[list[Application]] = relationship(back_populates="company")
    location: Mapped[str]


def create_db_tables(engine: Engine = engine):
    Base.metadata.create_all(engine)
