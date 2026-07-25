"""Reports the detected operating system version. Informational only."""

from __future__ import annotations

import platform

from app.services.audit.base import AuditCheck
from app.services.types import CheckFinding


class OsVersionCheck(AuditCheck):
    category = "os_version"

    def run_real(self) -> list[CheckFinding]:
        system = platform.system()
        release = platform.release()
        version = platform.version()
        return self._build_findings(f"{system} {release} (build {version})", source="real")

    def run_simulated(self) -> list[CheckFinding]:
        return self._build_findings("Windows 11 (build 22631)", source="simulated")

    def _build_findings(self, description: str, source: str) -> list[CheckFinding]:
        return [
            CheckFinding(
                category=self.category,
                status="info",
                severity="Info",
                description=f"Detected operating system: {description}.",
                evidence=description,
                recommendation="Keep the operating system updated via Windows Update.",
                weight=0.0,
                source=source,
            )
        ]
