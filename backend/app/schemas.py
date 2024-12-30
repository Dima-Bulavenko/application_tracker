# mypy: disable-error-code=assignment
from __future__ import annotations

from datetime import datetime
from typing import cast

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

from .db.models import AppStatus, WorkLocation, WorkType


def remove_tdo_suffix(class_obj: type):
    suffix = "dto"
    class_name = class_obj.__name__
    return (
        class_name[: -len(suffix)]
        if class_name.lower().endswith(suffix)
        else class_name
    )


class Model(BaseModel):
    model_config = ConfigDict(model_title_generator=remove_tdo_suffix)

    @field_validator("*", mode="before")
    @classmethod
    def empty_str_to_none[T](cls, v: T) -> T | None:
        if isinstance(v, str):
            return cast(T, v.strip()) or None
        return v


class ApplicationBaseDTO(Model):
    role: str = Field(max_length=40)
    work_type: "WorkType" = WorkType.FULL_TIME
    work_location: "WorkLocation" = WorkLocation.ON_SITE
    application_url: HttpUrl | None = None
    notes: str | None = Field(max_length=2000, default=None)
    interview_date: datetime | None = None


class ApplicationCreateDTO(ApplicationBaseDTO):
    company: "CompanyCreateDTO"


class ApplicationReadDTO(ApplicationBaseDTO):
    id: int
    status: "AppStatus" = AppStatus.APPLIED
    time_create: datetime
    time_update: datetime


class ApplicationUpdateDTO(ApplicationBaseDTO):
    role: str | None = Field(min_length=1, max_length=40, default=None)
    status: "AppStatus | None" = None
    work_type: "WorkType | None" = None
    work_location: "WorkLocation | None" = None
    notes: str | None = None
    application_url: HttpUrl | None = None
    company: "CompanyReadDTO | None" = None
    interview_date: datetime | None = None


class ApplicationReadRelDTO(ApplicationReadDTO):
    company: "CompanyReadDTO"


class CompanyBaseDTO(Model):
    name: str = Field(min_length=1, max_length=40)


class CompanyReadDTO(CompanyBaseDTO):
    id: int


class CompanyCreateDTO(CompanyBaseDTO):
    pass


class CompanyUpdateDTO(CompanyBaseDTO):
    name: str | None = Field(min_length=1, max_length=40, default=None)


class CompanyRelDTO(CompanyReadDTO):
    applications: list["ApplicationReadDTO"]
