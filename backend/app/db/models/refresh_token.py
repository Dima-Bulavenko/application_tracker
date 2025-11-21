from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .config import Base, pk_tp


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id: Mapped[pk_tp]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), index=True)
    token_hash: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    family_id: Mapped[str] = mapped_column(String(64), index=True)
    parent_token_id: Mapped[int | None] = mapped_column(
        ForeignKey("refresh_token.id", ondelete="SET NULL"), nullable=True, index=True
    )
    # Store timezone-aware datetimes to avoid mixing naive/aware values
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    time_create: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.current_timestamp())
    time_update: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.current_timestamp(), server_onupdate=func.current_timestamp()
    )
