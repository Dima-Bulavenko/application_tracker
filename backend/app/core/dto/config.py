# mypy: disable-error-code=assignment
from __future__ import annotations

from typing import cast

from pydantic import BaseModel, ConfigDict, Field, field_validator


def remove_tdo_suffix(class_obj: type):
    suffix = "dto"
    class_name = class_obj.__name__
    return class_name[: -len(suffix)] if class_name.lower().endswith(suffix) else class_name


class BaseModelDTO(BaseModel):
    model_config = ConfigDict(
        model_title_generator=remove_tdo_suffix,
        from_attributes=True,
        regex_engine="python-re",
    )

    @field_validator("*", mode="before")
    @classmethod
    def empty_str_to_none[T](cls, v: T) -> T | None:
        if isinstance(v, str):
            return cast(T, v.strip()) or None
        return v


class GenericFilterParams(BaseModelDTO):
    limit: int = Field(10, ge=1, le=50, description="Number of items to return")
    offset: int = Field(0, ge=0, description="Number of items to skip before starting to collect the result set")
