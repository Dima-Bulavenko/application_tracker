from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .config import Base, pk_tp


class VerificationToken(Base):
    __tablename__ = "verification_token"

    id: Mapped[pk_tp]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), index=True)
    token_hash: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    # Store timezone-aware datetimes to avoid mixing naive/aware values
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    time_create: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.current_timestamp())
    time_update: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.current_timestamp(), server_onupdate=func.current_timestamp()
    )
