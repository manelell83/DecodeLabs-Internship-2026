"""Endpoints for triggering and retrieving workstation security audits."""

from __future__ import annotations

import logging

from fastapi import APIRouter, Query

from app.api.deps import AuditServiceDep
from app.schemas.audit import AuditCreate, AuditDetail, AuditListResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/audits", tags=["audits"])


@router.post("", response_model=AuditDetail, status_code=201)
def create_audit(payload: AuditCreate, audit_service: AuditServiceDep) -> AuditDetail:
    """Run a new security audit (real or demo mode) and persist the result."""
    audit_run = audit_service.run_and_store(payload.mode)
    return AuditDetail.model_validate(audit_run, from_attributes=True)


@router.get("", response_model=AuditListResponse)
def list_audits(
    audit_service: AuditServiceDep,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    level: str | None = Query(default=None),
) -> AuditListResponse:
    """List past audit runs with pagination and optional level filtering."""
    items, total = audit_service.list_audits(page=page, page_size=page_size, level=level)
    return AuditListResponse(total=total, page=page, page_size=page_size, items=items)


@router.get("/{audit_id}", response_model=AuditDetail)
def get_audit(audit_id: int, audit_service: AuditServiceDep) -> AuditDetail:
    """Retrieve full detail for a single audit run, including all findings."""
    audit_run = audit_service.get_audit(audit_id)
    return AuditDetail.model_validate(audit_run, from_attributes=True)


@router.delete("/{audit_id}", status_code=204, response_model=None)
def delete_audit(audit_id: int, audit_service: AuditServiceDep) -> None:
    """Delete an audit run and its findings."""
    audit_service.delete_audit(audit_id)
