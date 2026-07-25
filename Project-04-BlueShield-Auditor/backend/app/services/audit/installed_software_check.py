"""Enumerates installed software via the Windows registry Uninstall keys."""

from __future__ import annotations

from app.services.audit.base import AuditCheck
from app.services.types import CheckFinding

_UNINSTALL_PATHS = (
    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
    r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
)


class InstalledSoftwareCheck(AuditCheck):
    category = "installed_software"

    def run_real(self) -> list[CheckFinding]:
        import winreg  # Windows-only; imported lazily so this module still loads elsewhere.

        names: list[str] = []
        for path in _UNINSTALL_PATHS:
            names.extend(self._read_display_names(winreg, path))

        return self._build_findings(sorted(set(names)), source="real")

    def run_simulated(self) -> list[CheckFinding]:
        return self._build_findings(
            ["Google Chrome", "7-Zip", "Microsoft Visual C++ Redistributable", "Zoom", "Slack"],
            source="simulated",
        )

    @staticmethod
    def _read_display_names(winreg_module, path: str) -> list[str]:
        names: list[str] = []
        try:
            with winreg_module.OpenKey(winreg_module.HKEY_LOCAL_MACHINE, path) as root_key:
                subkey_count = winreg_module.QueryInfoKey(root_key)[0]
                for i in range(subkey_count):
                    subkey_name = winreg_module.EnumKey(root_key, i)
                    try:
                        with winreg_module.OpenKey(root_key, subkey_name) as subkey:
                            display_name, _ = winreg_module.QueryValueEx(subkey, "DisplayName")
                            if display_name:
                                names.append(str(display_name))
                    except OSError:
                        continue
        except OSError:
            pass
        return names

    def _build_findings(self, names: list[str], source: str) -> list[CheckFinding]:
        preview = ", ".join(names[:8]) + (f" (+{len(names) - 8} more)" if len(names) > 8 else "")
        return [
            CheckFinding(
                category=self.category,
                status="info",
                severity="Info",
                description=f"{len(names)} installed application(s) detected.",
                evidence=preview or "No installed applications detected.",
                recommendation="Periodically review installed software and remove anything unused or untrusted.",
                weight=0.0,
                source=source,
            )
        ]
