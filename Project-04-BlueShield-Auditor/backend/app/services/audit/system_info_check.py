"""Reports basic system information. Informational only."""

from __future__ import annotations

import platform

import psutil

from app.services.audit.base import AuditCheck
from app.services.types import CheckFinding


class SystemInfoCheck(AuditCheck):
    category = "system_info"

    def run_real(self) -> list[CheckFinding]:
        memory_gb = round(psutil.virtual_memory().total / (1024**3), 1)
        evidence = (
            f"Hostname: {platform.node()} | Processor: {platform.processor() or 'Unknown'} | "
            f"RAM: {memory_gb} GB | CPU cores: {psutil.cpu_count(logical=True)}"
        )
        return self._build_findings(evidence, source="real")

    def run_simulated(self) -> list[CheckFinding]:
        evidence = "Hostname: DEMO-WORKSTATION | Processor: Simulated CPU | RAM: 16.0 GB | CPU cores: 8"
        return self._build_findings(evidence, source="simulated")

    def _build_findings(self, evidence: str, source: str) -> list[CheckFinding]:
        return [
            CheckFinding(
                category=self.category,
                status="info",
                severity="Info",
                description="System hardware information.",
                evidence=evidence,
                recommendation="No action needed.",
                weight=0.0,
                source=source,
            )
        ]
