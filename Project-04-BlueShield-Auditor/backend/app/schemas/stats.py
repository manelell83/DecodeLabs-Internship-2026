"""Pydantic schemas for dashboard/statistics aggregates."""

from pydantic import BaseModel


class LevelCount(BaseModel):
    level: str
    count: int


class CategoryFailureCount(BaseModel):
    category: str
    count: int


class TrendPoint(BaseModel):
    date: str
    audit_count: int
    average_score: float


class StatsResponse(BaseModel):
    total_audits: int
    average_score: float
    latest_score: float | None
    level_breakdown: list[LevelCount]
    top_failing_categories: list[CategoryFailureCount]
    trend: list[TrendPoint]
