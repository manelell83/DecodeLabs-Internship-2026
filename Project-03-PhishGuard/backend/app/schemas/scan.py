"""Pydantic schemas for scan creation and retrieval."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.indicator import IndicatorRead


class ScanCreate(BaseModel):
    """Payload for submitting an email for analysis."""

    raw_content: str = Field(..., min_length=1, description="Raw email text, headers optional.")
    sender: str | None = Field(default=None, max_length=255)
    subject: str | None = Field(default=None, max_length=500)

    @field_validator("raw_content")
    @classmethod
    def content_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("raw_content must not be blank.")
        return value


class ScanSummary(BaseModel):
    """Lightweight scan representation used in list views."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    sender: str | None
    subject: str | None
    risk_score: float
    risk_level: str
    urls_found: int
    domains_found: int


class ScanDetail(ScanSummary):
    """Full scan representation including raw content and indicators."""

    raw_content: str
    summary: str
    indicators: list[IndicatorRead]
    recommendations: list[str] = Field(default_factory=list)


class ScanListResponse(BaseModel):
    """Paginated list of scans."""

    total: int
    page: int
    page_size: int
    items: list[ScanSummary]
