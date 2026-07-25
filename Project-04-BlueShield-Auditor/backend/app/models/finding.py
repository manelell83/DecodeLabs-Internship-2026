"""ORM model for a single audit finding produced by one security check."""

from __future__ import annotations

from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Finding(Base):
    """A single check result (pass/warning/fail/info) within an audit run."""

    __tablename__ = "findings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    audit_run_id: Mapped[int] = mapped_column(ForeignKey("audit_runs.id"), index=True)

    category: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(20), default="info")
    severity: Mapped[str] = mapped_column(String(20), default="Info")
    description: Mapped[str] = mapped_column(Text)
    evidence: Mapped[str] = mapped_column(Text, default="")
    recommendation: Mapped[str] = mapped_column(Text, default="")
    weight: Mapped[float] = mapped_column(Float, default=0.0)
    source: Mapped[str] = mapped_column(String(10), default="real")

    audit_run: Mapped["AuditRun"] = relationship(back_populates="findings")
