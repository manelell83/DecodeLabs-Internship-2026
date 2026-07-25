"""Audits the local password policy via `secedit /export`.

`net accounts` prints its output in the OS display language (e.g. French:
"Longueur minimale du mot de passe"), which breaks keyword matching on
non-English Windows installs. `secedit /export` instead writes an INI file
with stable, locale-independent English key names (MinimumPasswordLength,
LockoutBadCount) regardless of the system's display language.
"""

from __future__ import annotations

import re
import tempfile
from pathlib import Path

from app.services.audit.base import AuditCheck
from app.services.types import CheckFinding

_MIN_LENGTH_PATTERN = re.compile(r"^MinimumPasswordLength\s*=\s*(\d+)", re.IGNORECASE | re.MULTILINE)
_LOCKOUT_PATTERN = re.compile(r"^LockoutBadCount\s*=\s*(\d+)", re.IGNORECASE | re.MULTILINE)

_RECOMMENDED_MIN_LENGTH = 8


class PasswordPolicyCheck(AuditCheck):
    category = "password_policy"

    def run_real(self) -> list[CheckFinding]:
        with tempfile.TemporaryDirectory() as tmp_dir:
            export_path = Path(tmp_dir) / "secpol.cfg"
            self._runner.run_shell(["secedit", "/export", "/cfg", str(export_path), "/quiet"])

            if not export_path.exists():
                raise ValueError("secedit did not produce a policy export file.")

            content = export_path.read_text(encoding="utf-16", errors="ignore")

        min_length_match = _MIN_LENGTH_PATTERN.search(content)
        lockout_match = _LOCKOUT_PATTERN.search(content)

        if not min_length_match:
            raise ValueError("Could not parse MinimumPasswordLength from secedit export.")

        min_length = int(min_length_match.group(1))
        lockout_threshold = lockout_match.group(1) if lockout_match else "0"

        return self._build_findings(min_length, lockout_threshold, source="real")

    def run_simulated(self) -> list[CheckFinding]:
        return self._build_findings(min_length=8, lockout_threshold="5", source="simulated")

    def _build_findings(self, min_length: int, lockout_threshold: str, source: str) -> list[CheckFinding]:
        findings: list[CheckFinding] = []

        if min_length < _RECOMMENDED_MIN_LENGTH:
            findings.append(
                CheckFinding(
                    category=self.category,
                    status="fail",
                    severity="High",
                    description=f"Minimum password length is only {min_length} characters.",
                    evidence=f"Minimum password length: {min_length}",
                    recommendation=f"Set the minimum password length to at least {_RECOMMENDED_MIN_LENGTH} characters via Local Security Policy.",
                    weight=12.0,
                    source=source,
                )
            )
        else:
            findings.append(
                CheckFinding(
                    category=self.category,
                    status="pass",
                    severity="Info",
                    description=f"Minimum password length meets the recommended baseline ({min_length} characters).",
                    evidence=f"Minimum password length: {min_length}",
                    recommendation="No action needed.",
                    weight=0.0,
                    source=source,
                )
            )

        lockout_count = int(lockout_threshold) if lockout_threshold.isdigit() else 0
        if lockout_count == 0:
            findings.append(
                CheckFinding(
                    category=self.category,
                    status="warning",
                    severity="Medium",
                    description="Account lockout threshold is not configured, allowing unlimited login attempts.",
                    evidence=f"Lockout threshold: {lockout_threshold}",
                    recommendation="Configure an account lockout threshold (e.g. 5 attempts) to slow brute-force attacks.",
                    weight=8.0,
                    source=source,
                )
            )
        else:
            findings.append(
                CheckFinding(
                    category=self.category,
                    status="pass",
                    severity="Info",
                    description=f"Account lockout threshold is configured ({lockout_threshold} attempts).",
                    evidence=f"Lockout threshold: {lockout_threshold}",
                    recommendation="No action needed.",
                    weight=0.0,
                    source=source,
                )
            )

        return findings
