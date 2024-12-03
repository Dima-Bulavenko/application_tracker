import datetime
import enum
from typing import Annotated

from sqlalchemy import DateTime, Enum, func
from sqlalchemy.orm import DeclarativeBase, mapped_column

time_create_tp = Annotated(
    datetime.datetime,
    mapped_column(DateTime(timezone=True), server_default=func.now()),
)

time_update_tp = Annotated(
    datetime.datetime,
    mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
    ),
)

pk_tp = Annotated(int, mapped_column(primary_key=True))


class Base(DeclarativeBase):
    type_annotation_map = {
        enum.Enum: Enum(values_callable=lambda x: [e.value for e in x])
    }

    repr_num_cols = 2
    repr_additional_cols = ()

    def __repr__(self):
        cols = []
        for inx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_additional_cols or inx < self.repr_num_cols:
                cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {", ".join(cols)}>"
