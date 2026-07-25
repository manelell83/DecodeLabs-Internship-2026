"""Endpoints for generating and downloading JSON/PDF audit reports."""

from __future__ import annotations

import logging
from typing import Literal

from fastapi import APIRouter, Query
from fastapi.responses import FileResponse, JSONResponse

from app.api.deps import AuditServiceDep, ReportGeneratorDep

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/audits", tags=["reports"])


@router.get("/{audit_id}/report")
def get_audit_report(
    audit_id: int,
    audit_service: AuditServiceDep,
    report_generator: ReportGeneratorDep,
    format: Literal["json", "pdf"] = Query(default="json"),
):
    """Generate (or regenerate) and return a report for the given audit run."""
    audit_run = audit_service.get_audit(audit_id)

    if format == "json":
        return JSONResponse(content=report_generator.build_json(audit_run))

    pdf_path = report_generator.write_pdf(audit_run)
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"blueshield_audit_{audit_id}.pdf",
    )
