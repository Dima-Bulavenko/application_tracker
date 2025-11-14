from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, sql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .config import Base, pk_tp, time_create_tp, time_update_tp

if TYPE_CHECKING:
    from .application import Application


class User(Base):
    __tablename__ = "user"
    id: Mapped[pk_tp]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    first_name: Mapped[str | None] = mapped_column(String(40))
    second_name: Mapped[str | None] = mapped_column(String(40))
    time_create: Mapped[time_create_tp]
    time_update: Mapped[time_update_tp]
    is_active: Mapped[bool] = mapped_column(default=False, server_default=sql.false())
    applications: Mapped[list["Application"]] = relationship(back_populates="user")
