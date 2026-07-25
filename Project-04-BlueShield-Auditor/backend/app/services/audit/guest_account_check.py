"""Audits whether the built-in Guest account is enabled."""

from __future__ import annotations

import json

from app.services.audit.base import AuditCheck
from app.services.types import CheckFinding


class GuestAccountCheck(AuditCheck):
    category = "guest_account"

    def run_real(self) -> list[CheckFinding]:
        # The built-in Guest account always has the well-known relative ID 501.
        # Matching by SID suffix instead of the literal name "Guest" makes this
        # locale-independent — on non-English Windows installs (e.g. French:
        # "Invité") the English name doesn't exist.
        output = self._runner.run_powershell(
            "Get-LocalUser | Where-Object { $_.SID.Value -like '*-501' } | "
            "Select-Object -ExpandProperty Enabled | ConvertTo-Json -Compress"
        )
        if not output:
            raise ValueError("Guest account status could not be determined.")

        enabled = bool(json.loads(output.lower()))
        return self._build_findings(enabled, source="real")

    def run_simulated(self) -> list[CheckFinding]:
        return self._build_findings(enabled=False, source="simulated")

    def _build_findings(self, enabled: bool, source: str) -> list[CheckFinding]:
        if enabled:
            return [
                CheckFinding(
                    category=self.category,
                    status="fail",
                    severity="High",
                    description="The built-in Guest account is enabled, allowing anonymous local access.",
                    evidence="Guest account: Enabled",
                    recommendation="Disable the Guest account via Local Users and Groups (lusrmgr.msc).",
                    weight=15.0,
                    source=source,
                )
            ]

        return [
            CheckFinding(
                category=self.category,
                status="pass",
                severity="Info",
                description="The built-in Guest account is disabled.",
                evidence="Guest account: Disabled",
                recommendation="No action needed.",
                weight=0.0,
                source=source,
            )
        ]
