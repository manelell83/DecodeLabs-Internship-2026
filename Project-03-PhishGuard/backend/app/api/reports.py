"""Endpoints for generating and downloading JSON/PDF scan reports."""

from __future__ import annotations

import logging
from typing import Literal

from fastapi import APIRouter, Query
from fastapi.responses import FileResponse, JSONResponse

from app.api.deps import ReportGeneratorDep, ScanServiceDep

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/scans", tags=["reports"])


@router.get("/{scan_id}/report")
def get_scan_report(
    scan_id: int,
    scan_service: ScanServiceDep,
    report_generator: ReportGeneratorDep,
    format: Literal["json", "pdf"] = Query(default="json"),
):
    """Generate (or regenerate) and return a report for the given scan."""
    scan = scan_service.get_scan(scan_id)

    if format == "json":
        return JSONResponse(content=report_generator.build_json(scan))

    pdf_path = report_generator.write_pdf(scan)
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"phishguard_scan_{scan_id}.pdf",
    )
