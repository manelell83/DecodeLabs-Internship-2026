"""Shared FastAPI dependencies for API routers."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.database.session import get_db
from app.services.report_generator import ReportGenerator
from app.services.scan_service import ScanService
from app.services.stats_service import StatsService

DbSession = Annotated[Session, Depends(get_db)]


def get_scan_service(db: DbSession) -> ScanService:
    """Provide a request-scoped ScanService bound to the request's DB session."""
    return ScanService(db)


def get_stats_service(db: DbSession) -> StatsService:
    """Provide a request-scoped StatsService bound to the request's DB session."""
    return StatsService(db)


def get_report_generator(settings: Annotated[Settings, Depends(get_settings)]) -> ReportGenerator:
    """Provide a ReportGenerator configured with the app's reports directory."""
    return ReportGenerator(settings.reports_dir)


ScanServiceDep = Annotated[ScanService, Depends(get_scan_service)]
StatsServiceDep = Annotated[StatsService, Depends(get_stats_service)]
ReportGeneratorDep = Annotated[ReportGenerator, Depends(get_report_generator)]

