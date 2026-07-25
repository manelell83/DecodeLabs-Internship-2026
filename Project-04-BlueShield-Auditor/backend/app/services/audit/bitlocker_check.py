"""Audits BitLocker drive encryption status on the system drive, when available.

BitLocker is legitimately unavailable on many machines (Windows Home edition,
missing TPM, or the process lacking admin rights). That's not a security
failure in itself, so an unavailable result is reported honestly as such
rather than being penalized or silently swapped for fabricated demo data.
"""

from __future__ import annotations

import re

from app.services.audit.base import AuditCheck
from app.services.audit.command_runner import CommandError
from app.services.types import CheckFinding

_STATUS_PATTERN = re.compile(r"Conversion Status:\s*(.+)", re.IGNORECASE)


class BitLockerCheck(AuditCheck):
    category = "bitlocker"

    def run_real(self) -> list[CheckFinding]:
        try:
            output = self._runner.run_shell(["manage-bde", "-status", "C:"])
        except CommandError:
            return [self._unavailable_finding(source="real")]

        match = _STATUS_PATTERN.search(output)
        if not match:
            return [self._unavailable_finding(source="real")]

        status_text = match.group(1).strip()
        return self._build_findings(status_text, source="real")

    def run_simulated(self) -> list[CheckFinding]:
        return self._build_findings("Fully Encrypted", source="simulated")

    def _unavailable_finding(self, source: str) -> CheckFinding:
        return CheckFinding(
            category=self.category,
            status="unavailable",
            severity="Info",
            description="BitLocker status could not be determined on this system.",
            evidence="manage-bde reported no accessible status (may require admin rights, or BitLocker is unsupported on this edition).",
            recommendation="If this device handles sensitive data, verify BitLocker or device encryption is available and enabled.",
            weight=0.0,
            source=source,
        )

    def _build_findings(self, status_text: str, source: str) -> list[CheckFinding]:
        if "fully encrypted" in status_text.lower():
            return [
                CheckFinding(
                    category=self.category,
                    status="pass",
                    severity="Info",
                    description="The system drive is fully encrypted with BitLocker.",
                    evidence=f"Conversion Status: {status_text}",
                    recommendation="No action needed.",
                    weight=0.0,
                    source=source,
                )
            ]

        return [
            CheckFinding(
                category=self.category,
                status="warning",
                severity="Medium",
                description="The system drive is not fully encrypted with BitLocker.",
                evidence=f"Conversion Status: {status_text}",
                recommendation="Enable BitLocker on the system drive to protect data if the device is lost or stolen.",
                weight=10.0,
                source=source,
            )
        ]
