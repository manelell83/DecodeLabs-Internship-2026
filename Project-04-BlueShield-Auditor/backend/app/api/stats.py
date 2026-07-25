"""Endpoints exposing aggregate dashboard/statistics data."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.deps import StatsServiceDep
from app.schemas.stats import StatsResponse

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("", response_model=StatsResponse)
def get_stats(stats_service: StatsServiceDep) -> StatsResponse:
    """Return aggregate statistics for the dashboard and statistics pages."""
    return stats_service.get_stats()
