"""Endpoints for submitting and retrieving phishing email scans."""

from __future__ import annotations

import logging

from fastapi import APIRouter, Query

from app.api.deps import ScanServiceDep
from app.schemas.scan import ScanCreate, ScanDetail, ScanListResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/scans", tags=["scans"])


@router.post("", response_model=ScanDetail, status_code=201)
def create_scan(payload: ScanCreate, scan_service: ScanServiceDep) -> ScanDetail:
    """Analyze a submitted email and persist the resulting scan."""
    scan = scan_service.analyze_and_store(payload)
    return ScanDetail.model_validate(scan, from_attributes=True)


@router.get("", response_model=ScanListResponse)
def list_scans(
    scan_service: ScanServiceDep,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None),
    risk_level: str | None = Query(default=None),
) -> ScanListResponse:
    """List scan history with pagination, search, and risk-level filtering."""
    items, total = scan_service.list_scans(page=page, page_size=page_size, search=search, risk_level=risk_level)
    return ScanListResponse(total=total, page=page, page_size=page_size, items=items)


@router.get("/{scan_id}", response_model=ScanDetail)
def get_scan(scan_id: int, scan_service: ScanServiceDep) -> ScanDetail:
    """Retrieve full detail for a single scan, including indicators and recommendations."""
    scan = scan_service.get_scan(scan_id)
    return ScanDetail.model_validate(scan, from_attributes=True)


@router.delete("/{scan_id}", status_code=204, response_model=None)
def delete_scan(scan_id: int, scan_service: ScanServiceDep) -> None:
    """Delete a scan and its associated indicators/reports."""
    scan_service.delete_scan(scan_id)
