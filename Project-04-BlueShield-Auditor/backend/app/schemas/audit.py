"""Pydantic schemas for audit run creation and retrieval."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

from app.schemas.finding import FindingRead

AuditMode = Literal["real", "demo"]


class AuditCreate(BaseModel):
    """Payload for triggering a new audit run."""

    mode: AuditMode = "real"


class AuditSummary(BaseModel):
    """Lightweight audit run representation used in list views."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    mode: str
    hostname: str | None
    os_summary: str | None
    score: float
    level: str


class AuditDetail(AuditSummary):
    """Full audit run representation including all findings."""

    summary: str
    findings: list[FindingRead]


class AuditListResponse(BaseModel):
    """Paginated list of audit runs."""

    total: int
    page: int
    page_size: int
    items: list[AuditSummary]
