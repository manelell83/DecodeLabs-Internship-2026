"""Computes dashboard statistics via aggregate queries over audit runs and findings."""

from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.audit_run import AuditRun
from app.models.finding import Finding
from app.schemas.stats import CategoryFailureCount, LevelCount, StatsResponse, TrendPoint


class StatsService:
    """Aggregates audit run and finding data for dashboard and statistics views."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def get_stats(self) -> StatsResponse:
        total_audits = self._db.query(func.count(AuditRun.id)).scalar() or 0
        average_score = self._db.query(func.avg(AuditRun.score)).scalar() or 0.0

        latest = self._db.query(AuditRun.score).order_by(AuditRun.created_at.desc()).first()
        latest_score = latest[0] if latest else None

        level_rows = self._db.query(AuditRun.level, func.count(AuditRun.id)).group_by(AuditRun.level).all()
        level_breakdown = [LevelCount(level=level, count=count) for level, count in level_rows]

        category_rows = (
            self._db.query(Finding.category, func.count(Finding.id))
            .filter(Finding.status.in_(["warning", "fail"]))
            .group_by(Finding.category)
            .order_by(func.count(Finding.id).desc())
            .limit(10)
            .all()
        )
        top_failing_categories = [
            CategoryFailureCount(category=category, count=count) for category, count in category_rows
        ]

        trend_rows = (
            self._db.query(
                func.date(AuditRun.created_at).label("day"),
                func.count(AuditRun.id),
                func.avg(AuditRun.score),
            )
            .group_by("day")
            .order_by("day")
            .limit(30)
            .all()
        )
        trend = [
            TrendPoint(date=str(day), audit_count=count, average_score=round(avg_score or 0.0, 1))
            for day, count, avg_score in trend_rows
        ]

        return StatsResponse(
            total_audits=total_audits,
            average_score=round(average_score, 1),
            latest_score=round(latest_score, 1) if latest_score is not None else None,
            level_breakdown=level_breakdown,
            top_failing_categories=top_failing_categories,
            trend=trend,
        )
