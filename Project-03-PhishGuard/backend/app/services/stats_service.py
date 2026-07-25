"""Computes dashboard statistics via aggregate queries over scans and indicators."""

from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.indicator import Indicator
from app.models.scan import Scan
from app.schemas.stats import CategoryCount, RiskLevelCount, StatsResponse, TrendPoint


class StatsService:
    """Aggregates scan and indicator data for dashboard and statistics views."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def get_stats(self) -> StatsResponse:
        total_scans = self._db.query(func.count(Scan.id)).scalar() or 0
        average_score = self._db.query(func.avg(Scan.risk_score)).scalar() or 0.0
        high_risk_count = (
            self._db.query(func.count(Scan.id)).filter(Scan.risk_level.in_(["High", "Critical"])).scalar() or 0
        )

        risk_breakdown_rows = (
            self._db.query(Scan.risk_level, func.count(Scan.id)).group_by(Scan.risk_level).all()
        )
        risk_breakdown = [RiskLevelCount(risk_level=level, count=count) for level, count in risk_breakdown_rows]

        category_rows = (
            self._db.query(Indicator.category, func.count(Indicator.id))
            .group_by(Indicator.category)
            .order_by(func.count(Indicator.id).desc())
            .limit(10)
            .all()
        )
        top_categories = [CategoryCount(category=category, count=count) for category, count in category_rows]

        trend_rows = (
            self._db.query(
                func.date(Scan.created_at).label("day"),
                func.count(Scan.id),
                func.avg(Scan.risk_score),
            )
            .group_by("day")
            .order_by("day")
            .limit(30)
            .all()
        )
        trend = [
            TrendPoint(date=str(day), scan_count=count, average_score=round(avg_score or 0.0, 1))
            for day, count, avg_score in trend_rows
        ]

        return StatsResponse(
            total_scans=total_scans,
            average_score=round(average_score, 1),
            high_risk_count=high_risk_count,
            risk_level_breakdown=risk_breakdown,
            top_categories=top_categories,
            trend=trend,
        )
