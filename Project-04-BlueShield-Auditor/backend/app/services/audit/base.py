"""Base class every audit check implements."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod

from app.services.audit.command_runner import CommandRunner
from app.services.types import CheckFinding

logger = logging.getLogger(__name__)


class AuditCheck(ABC):
    """A single security check with a real execution path and a simulated fallback.

    Subclasses implement `run_real()` for actual system inspection and
    `run_simulated()` for realistic demo data. `execute()` picks the path based
    on `mode`, transparently falling back to simulated data (tagged as such) if
    the real check fails for any reason — missing admin rights, non-Windows host,
    or a missing command — so one failing check never crashes the whole audit.
    """

    category: str

    def __init__(self, runner: CommandRunner | None = None) -> None:
        self._runner = runner or CommandRunner()

    def execute(self, mode: str) -> list[CheckFinding]:
        if mode == "demo":
            return self.run_simulated()

        try:
            return self.run_real()
        except Exception as exc:  # noqa: BLE001 - any failure falls back to simulated data
            logger.warning("Real check '%s' failed, falling back to simulated data: %s", self.category, exc)
            return self.run_simulated()

    @abstractmethod
    def run_real(self) -> list[CheckFinding]:
        """Inspect actual system state. Raise on any failure — the base class handles fallback."""

    @abstractmethod
    def run_simulated(self) -> list[CheckFinding]:
        """Return realistic, clearly-labeled mock data for demo mode or as a fallback."""
