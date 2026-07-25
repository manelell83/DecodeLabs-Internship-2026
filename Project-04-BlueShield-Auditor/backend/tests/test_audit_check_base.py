"""Tests the AuditCheck base class's real->simulated fallback behavior."""

from app.services.audit.base import AuditCheck
from app.services.types import CheckFinding


class _AlwaysFailsCheck(AuditCheck):
    category = "flaky"

    def run_real(self) -> list[CheckFinding]:
        raise RuntimeError("simulated environment failure (e.g. no admin rights)")

    def run_simulated(self) -> list[CheckFinding]:
        return [
            CheckFinding(
                category=self.category,
                status="pass",
                severity="Info",
                description="simulated result",
                evidence="e",
                recommendation="r",
                weight=0.0,
                source="simulated",
            )
        ]


class _AlwaysPassesCheck(AuditCheck):
    category = "reliable"

    def run_real(self) -> list[CheckFinding]:
        return [
            CheckFinding(
                category=self.category,
                status="pass",
                severity="Info",
                description="real result",
                evidence="e",
                recommendation="r",
                weight=0.0,
                source="real",
            )
        ]

    def run_simulated(self) -> list[CheckFinding]:
        raise AssertionError("should not be called when real mode succeeds")


def test_real_mode_falls_back_to_simulated_on_failure():
    findings = _AlwaysFailsCheck().execute("real")
    assert len(findings) == 1
    assert findings[0].source == "simulated"


def test_real_mode_uses_real_result_when_it_succeeds():
    findings = _AlwaysPassesCheck().execute("real")
    assert findings[0].source == "real"


def test_demo_mode_always_uses_simulated_path():
    findings = _AlwaysFailsCheck().execute("demo")
    assert findings[0].source == "simulated"
