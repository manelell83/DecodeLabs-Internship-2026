"""Pydantic schemas for phishing indicators."""

from pydantic import BaseModel, ConfigDict


class IndicatorRead(BaseModel):
    """Representation of a triggered indicator returned to clients."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    category: str
    description: str
    evidence: str
    severity: str
    weight: float
