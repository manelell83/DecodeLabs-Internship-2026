"""Audits the number of local Administrator group members via PowerShell."""

from __future__ import annotations

import json

from app.services.audit.base import AuditCheck
from app.services.types import CheckFinding

_RECOMMENDED_MAX_ADMINS = 2

# Well-known SID for the built-in Administrators group. Using the SID instead of
# the literal name "Administrators" makes this locale-independent — on non-English
# Windows installs (e.g. French: "Administrateurs") the English name doesn't exist.
_ADMINISTRATORS_GROUP_SID = "S-1-5-32-544"


class AdminAccountsCheck(AuditCheck):
    category = "admin_accounts"

    def run_real(self) -> list[CheckFinding]:
        output = self._runner.run_powershell(
            f"Get-LocalGroupMember -SID {_ADMINISTRATORS_GROUP_SID} | "
            "Select-Object -ExpandProperty Name | ConvertTo-Json -Compress"
        )
        names = self._parse_names(output)
        return self._build_findings(names, source="real")

    def run_simulated(self) -> list[CheckFinding]:
        return self._build_findings(["WORKGROUP\\Administrator", "WORKGROUP\\LocalAdmin"], source="simulated")

    @staticmethod
    def _parse_names(output: str) -> list[str]:
        if not output:
            return []
        parsed = json.loads(output)
        if isinstance(parsed, str):
            return [parsed]
        return list(parsed)

    def _build_findings(self, admin_names: list[str], source: str) -> list[CheckFinding]:
        count = len(admin_names)
        evidence = ", ".join(admin_names) if admin_names else "No administrator accounts found"

        if count > _RECOMMENDED_MAX_ADMINS:
            return [
                CheckFinding(
                    category=self.category,
                    status="warning",
                    severity="Medium",
                    description=f"{count} accounts have local Administrator privileges — more than recommended.",
                    evidence=evidence,
                    recommendation="Review the Administrators group and remove accounts that don't need elevated privileges.",
                    weight=10.0,
                    source=source,
                )
            ]

        return [
            CheckFinding(
                category=self.category,
                status="pass",
                severity="Info",
                description=f"{count} account(s) hold local Administrator privileges.",
                evidence=evidence,
                recommendation="No action needed.",
                weight=0.0,
                source=source,
            )
        ]
