"""ORM model for a single phishing indicator triggered during a scan."""

from __future__ import annotations

from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Indicator(Base):
    """A single suspicious signal detected within a scan."""

    __tablename__ = "indicators"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey("scans.id"), index=True)

    category: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)
    evidence: Mapped[str] = mapped_column(Text, default="")
    severity: Mapped[str] = mapped_column(String(20), default="Medium")
    weight: Mapped[float] = mapped_column(Float, default=0.0)

    scan: Mapped["Scan"] = relationship(back_populates="indicators")
