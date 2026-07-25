"""Pydantic schemas for dashboard/statistics aggregates."""

from pydantic import BaseModel


class RiskLevelCount(BaseModel):
    risk_level: str
    count: int


class CategoryCount(BaseModel):
    category: str
    count: int


class TrendPoint(BaseModel):
    date: str
    scan_count: int
    average_score: float


class StatsResponse(BaseModel):
    total_scans: int
    average_score: float
    high_risk_count: int
    risk_level_breakdown: list[RiskLevelCount]
    top_categories: list[CategoryCount]
    trend: list[TrendPoint]
