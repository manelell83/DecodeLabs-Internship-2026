"""ORM model for a single email scan."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Scan(Base):
    """A single phishing analysis run against one email."""

    __tablename__ = "scans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), index=True
    )

    sender: Mapped[str | None] = mapped_column(String(255), nullable=True)
    subject: Mapped[str | None] = mapped_column(String(500), nullable=True)
    raw_content: Mapped[str] = mapped_column(Text)

    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    risk_level: Mapped[str] = mapped_column(String(20), default="Low")
    summary: Mapped[str] = mapped_column(Text, default="")

    urls_found: Mapped[int] = mapped_column(Integer, default=0)
    domains_found: Mapped[int] = mapped_column(Integer, default=0)

    indicators: Mapped[list["Indicator"]] = relationship(
        back_populates="scan", cascade="all, delete-orphan", lazy="selectin"
    )
    reports: Mapped[list["Report"]] = relationship(
        back_populates="scan", cascade="all, delete-orphan", lazy="selectin"
    )
