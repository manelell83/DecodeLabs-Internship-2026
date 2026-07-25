"""Orchestrates running all audit checks and persisting the resulting audit run."""

from __future__ import annotations

import logging
import platform

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.exceptions import AuditRunNotFoundError, InvalidAuditModeError
from app.models.audit_run import AuditRun
from app.models.finding import Finding
from app.services.audit.admin_accounts_check import AdminAccountsCheck
from app.services.audit.base import AuditCheck
from app.services.audit.bitlocker_check import BitLockerCheck
from app.services.audit.defender_check import DefenderCheck
from app.services.audit.firewall_check import FirewallCheck
from app.services.audit.guest_account_check import GuestAccountCheck
from app.services.audit.installed_software_check import InstalledSoftwareCheck
from app.services.audit.os_version_check import OsVersionCheck
from app.services.audit.password_policy_check import PasswordPolicyCheck
from app.services.audit.system_info_check import SystemInfoCheck
from app.services.audit.windows_update_check import WindowsUpdateCheck
from app.services.audit_scorer import AuditScorer

logger = logging.getLogger(__name__)

_VALID_MODES = {"real", "demo"}


def _default_checks() -> list[AuditCheck]:
    return [
        PasswordPolicyCheck(),
        AdminAccountsCheck(),
        GuestAccountCheck(),
        DefenderCheck(),
        FirewallCheck(),
        BitLockerCheck(),
        WindowsUpdateCheck(),
        OsVersionCheck(),
        InstalledSoftwareCheck(),
        SystemInfoCheck(),
    ]


class AuditService:
    """Coordinates running audit checks, scoring, and persistence for audit runs."""

    def __init__(self, db: Session, checks: list[AuditCheck] | None = None) -> None:
        self._db = db
        self._checks = checks or _default_checks()
        self._scorer = AuditScorer()

    def run_and_store(self, mode: str) -> AuditRun:
        if mode not in _VALID_MODES:
            raise InvalidAuditModeError(mode)

        all_findings = []
        for check in self._checks:
            all_findings.extend(check.execute(mode))

        result = self._scorer.score(all_findings)

        audit_run = AuditRun(
            mode=mode,
            hostname=platform.node() or "Unknown",
            os_summary=f"{platform.system()} {platform.release()}".strip() or "Unknown",
            score=result.score,
            level=result.level,
            summary=result.summary,
        )
        audit_run.findings = [
            Finding(
                category=f.category,
                status=f.status,
                severity=f.severity,
                description=f.description,
                evidence=f.evidence,
                recommendation=f.recommendation,
                weight=f.weight,
                source=f.source,
            )
            for f in all_findings
        ]

        self._db.add(audit_run)
        self._db.commit()
        self._db.refresh(audit_run)
        logger.info("Audit run %s stored with score %s (%s)", audit_run.id, audit_run.score, audit_run.level)
        return audit_run

    def get_audit(self, audit_id: int) -> AuditRun:
        audit_run = self._db.get(AuditRun, audit_id)
        if audit_run is None:
            raise AuditRunNotFoundError(audit_id)
        return audit_run

    def list_audits(self, page: int, page_size: int, level: str | None = None) -> tuple[list[AuditRun], int]:
        query = self._db.query(AuditRun)
        if level:
            query = query.filter(AuditRun.level == level)
        total = query.with_entities(func.count(AuditRun.id)).scalar() or 0
        items = (
            query.order_by(AuditRun.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return items, total

    def delete_audit(self, audit_id: int) -> None:
        audit_run = self._db.get(AuditRun, audit_id)
        if audit_run is None:
            raise AuditRunNotFoundError(audit_id)
        self._db.delete(audit_run)
        self._db.commit()
