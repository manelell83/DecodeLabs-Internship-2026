"""Orchestrates the full email analysis pipeline and scan persistence."""

from __future__ import annotations

import logging

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.exceptions import EmptyEmailContentError, ScanNotFoundError
from app.models.indicator import Indicator
from app.models.scan import Scan
from app.schemas.scan import ScanCreate
from app.services.content_analyzer import ContentAnalyzer
from app.services.email_parser import EmailParser
from app.services.recommendation_engine import RecommendationEngine
from app.services.risk_scorer import RiskScorer
from app.services.url_analyzer import URLAnalyzer

logger = logging.getLogger(__name__)


class ScanService:
    """Coordinates parsing, analysis, scoring, and persistence for email scans."""

    def __init__(self, db: Session) -> None:
        self._db = db
        self._parser = EmailParser()
        self._url_analyzer = URLAnalyzer()
        self._content_analyzer = ContentAnalyzer()
        self._scorer = RiskScorer()
        self._recommender = RecommendationEngine()

    def analyze_and_store(self, payload: ScanCreate) -> Scan:
        if not payload.raw_content.strip():
            raise EmptyEmailContentError()

        parsed = self._parser.parse(payload.raw_content, sender=payload.sender, subject=payload.subject)
        sender_domain = parsed.sender.rsplit("@", 1)[-1].lower() if parsed.sender and "@" in parsed.sender else None

        indicator_hits = [
            *self._url_analyzer.analyze(parsed.urls),
            *self._content_analyzer.analyze(parsed.body, sender_domain),
        ]
        risk = self._scorer.score(indicator_hits)
        recommendations = self._recommender.generate(indicator_hits)

        scan = Scan(
            sender=parsed.sender,
            subject=parsed.subject,
            raw_content=payload.raw_content,
            risk_score=risk.score,
            risk_level=risk.level,
            summary=risk.summary,
            urls_found=len(parsed.urls),
            domains_found=len(parsed.domains),
        )
        scan.indicators = [
            Indicator(
                category=hit.category,
                description=hit.description,
                evidence=hit.evidence,
                severity=hit.severity,
                weight=hit.weight,
            )
            for hit in indicator_hits
        ]

        self._db.add(scan)
        self._db.commit()
        self._db.refresh(scan)
        logger.info("Scan %s stored with risk score %s (%s)", scan.id, scan.risk_score, scan.risk_level)

        scan.recommendations = recommendations  # transient attribute for the response schema
        return scan

    def get_scan(self, scan_id: int) -> Scan:
        scan = self._db.get(Scan, scan_id)
        if scan is None:
            raise ScanNotFoundError(scan_id)
        scan.recommendations = self._recommender.generate(scan.indicators)
        return scan

    def list_scans(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
        risk_level: str | None = None,
    ) -> tuple[list[Scan], int]:
        query = self._db.query(Scan)

        if search:
            like = f"%{search}%"
            query = query.filter((Scan.subject.ilike(like)) | (Scan.sender.ilike(like)))
        if risk_level:
            query = query.filter(Scan.risk_level == risk_level)

        total = query.with_entities(func.count(Scan.id)).scalar() or 0
        items = (
            query.order_by(Scan.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return items, total

    def delete_scan(self, scan_id: int) -> None:
        scan = self._db.get(Scan, scan_id)
        if scan is None:
            raise ScanNotFoundError(scan_id)
        self._db.delete(scan)
        self._db.commit()
