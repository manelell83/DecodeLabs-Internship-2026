"""Best-effort check of how recently Windows Updates were installed.

This is not authoritative for *pending* updates — determining that reliably
requires the Windows Update COM API or WSUS/enterprise tooling. Instead this
checks the most recent installed hotfix date via `Get-HotFix`, which is a
reasonable proxy: a machine with no updates in a long time is very likely
behind, even if we can't enumerate exactly what's missing.
"""

from __future__ import annotations

from datetime import datetime, timezone

from app.services.audit.base import AuditCheck
from app.services.types import CheckFinding

_STALE_THRESHOLD_DAYS = 60


class WindowsUpdateCheck(AuditCheck):
    category = "windows_update"

    def run_real(self) -> list[CheckFinding]:
        output = self._runner.run_powershell(
            "Get-HotFix -ErrorAction Stop | Sort-Object InstalledOn -Descending | "
            "Select-Object -First 1 -ExpandProperty InstalledOn | "
            "ForEach-Object { $_.ToString('yyyy-MM-dd') }"
        )
        if not output:
            raise ValueError("No installed hotfix history was found.")

        last_update = datetime.strptime(output, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        days_since = (datetime.now(timezone.utc) - last_update).days
        return self._build_findings(last_update.date().isoformat(), days_since, source="real")

    def run_simulated(self) -> list[CheckFinding]:
        return self._build_findings("recently", days_since=10, source="simulated")

    def _build_findings(self, last_update_label: str, days_since: int, source: str) -> list[CheckFinding]:
        if days_since > _STALE_THRESHOLD_DAYS:
            return [
                CheckFinding(
                    category=self.category,
                    status="warning",
                    severity="Medium",
                    description=f"No Windows Updates detected in the last {days_since} days.",
                    evidence=f"Last installed update: {last_update_label}",
                    recommendation="Run Windows Update and install any pending security patches.",
                    weight=10.0,
                    source=source,
                )
            ]

        return [
            CheckFinding(
                category=self.category,
                status="pass",
                severity="Info",
                description=f"Windows Updates appear current (last installed {days_since} day(s) ago).",
                evidence=f"Last installed update: {last_update_label}",
                recommendation="No action needed.",
                weight=0.0,
                source=source,
            )
        ]
