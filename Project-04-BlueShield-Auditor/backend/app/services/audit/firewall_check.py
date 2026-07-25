"""Audits Windows Firewall status across the Domain, Private, and Public profiles."""

from __future__ import annotations

import json

from app.services.audit.base import AuditCheck
from app.services.types import CheckFinding

_WEIGHT_PER_DISABLED_PROFILE = 10.0


class FirewallCheck(AuditCheck):
    category = "firewall"

    def run_real(self) -> list[CheckFinding]:
        output = self._runner.run_powershell(
            "Get-NetFirewallProfile -ErrorAction Stop | "
            "Select-Object Name, Enabled | ConvertTo-Json -Compress"
        )
        if not output:
            raise ValueError("Firewall profile status could not be determined.")

        data = json.loads(output)
        profiles = data if isinstance(data, list) else [data]
        statuses = {p["Name"]: bool(p["Enabled"]) for p in profiles}
        return self._build_findings(statuses, source="real")

    def run_simulated(self) -> list[CheckFinding]:
        return self._build_findings({"Domain": True, "Private": True, "Public": True}, source="simulated")

    def _build_findings(self, statuses: dict[str, bool], source: str) -> list[CheckFinding]:
        disabled = [name for name, enabled in statuses.items() if not enabled]
        evidence = ", ".join(f"{name}={'On' if enabled else 'Off'}" for name, enabled in statuses.items())

        if disabled:
            return [
                CheckFinding(
                    category=self.category,
                    status="fail",
                    severity="Critical" if len(disabled) == len(statuses) else "High",
                    description=f"Firewall is disabled on the following profile(s): {', '.join(disabled)}.",
                    evidence=evidence,
                    recommendation="Enable Windows Firewall for all network profiles via Windows Security settings.",
                    weight=_WEIGHT_PER_DISABLED_PROFILE * len(disabled),
                    source=source,
                )
            ]

        return [
            CheckFinding(
                category=self.category,
                status="pass",
                severity="Info",
                description="Windows Firewall is enabled on all network profiles.",
                evidence=evidence,
                recommendation="No action needed.",
                weight=0.0,
                source=source,
            )
        ]
