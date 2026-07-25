"""Audits Windows Defender antivirus and real-time protection status."""

from __future__ import annotations

import json

from app.services.audit.base import AuditCheck
from app.services.types import CheckFinding


class DefenderCheck(AuditCheck):
    category = "windows_defender"

    def run_real(self) -> list[CheckFinding]:
        output = self._runner.run_powershell(
            "Get-MpComputerStatus -ErrorAction Stop | "
            "Select-Object AntivirusEnabled, RealTimeProtectionEnabled | ConvertTo-Json -Compress"
        )
        if not output:
            raise ValueError("Windows Defender status could not be determined.")

        data = json.loads(output)
        return self._build_findings(
            antivirus_enabled=bool(data.get("AntivirusEnabled")),
            realtime_enabled=bool(data.get("RealTimeProtectionEnabled")),
            source="real",
        )

    def run_simulated(self) -> list[CheckFinding]:
        return self._build_findings(antivirus_enabled=True, realtime_enabled=True, source="simulated")

    def _build_findings(self, antivirus_enabled: bool, realtime_enabled: bool, source: str) -> list[CheckFinding]:
        if not antivirus_enabled or not realtime_enabled:
            return [
                CheckFinding(
                    category=self.category,
                    status="fail",
                    severity="Critical",
                    description="Windows Defender antivirus or real-time protection is disabled.",
                    evidence=f"AntivirusEnabled={antivirus_enabled}, RealTimeProtectionEnabled={realtime_enabled}",
                    recommendation="Enable Windows Defender and real-time protection via Windows Security settings.",
                    weight=20.0,
                    source=source,
                )
            ]

        return [
            CheckFinding(
                category=self.category,
                status="pass",
                severity="Info",
                description="Windows Defender antivirus and real-time protection are both active.",
                evidence="AntivirusEnabled=True, RealTimeProtectionEnabled=True",
                recommendation="No action needed.",
                weight=0.0,
                source=source,
            )
        ]
