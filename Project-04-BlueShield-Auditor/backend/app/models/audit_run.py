"""ORM model for a single workstation security audit run."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class AuditRun(Base):
    """A single security audit executed against the local workstation."""

    __tablename__ = "audit_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), index=True
    )

    mode: Mapped[str] = mapped_column(String(10), default="real")
    hostname: Mapped[str | None] = mapped_column(String(255), nullable=True)
    os_summary: Mapped[str | None] = mapped_column(String(255), nullable=True)

    score: Mapped[float] = mapped_column(Float, default=0.0)
    level: Mapped[str] = mapped_column(String(20), default="Poor")
    summary: Mapped[str] = mapped_column(Text, default="")

    findings: Mapped[list["Finding"]] = relationship(
        back_populates="audit_run", cascade="all, delete-orphan", lazy="selectin"
    )
