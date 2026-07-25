"""Pydantic schemas for audit findings."""

from pydantic import BaseModel, ConfigDict


class FindingRead(BaseModel):
    """Representation of a single check result returned to clients."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    category: str
    status: str
    severity: str
    description: str
    evidence: str
    recommendation: str
    weight: float
    source: str
