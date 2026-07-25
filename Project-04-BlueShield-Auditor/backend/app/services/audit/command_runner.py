"""Centralized, testable subprocess execution for Windows system commands.

All audit checks that need to shell out (PowerShell cmdlets, `net accounts`,
`manage-bde`, etc.) go through this one class so timeout handling, error capture,
and logging are consistent — and so tests can substitute a fake runner instead
of actually invoking PowerShell (which won't exist in a Linux CI container).
"""

from __future__ import annotations

import logging
import subprocess

logger = logging.getLogger(__name__)


class CommandError(Exception):
    """Raised when a system command fails, times out, or is unavailable on this host."""


class CommandRunner:
    """Runs PowerShell commands and returns their stdout, raising CommandError on failure."""

    def __init__(self, timeout_seconds: int = 15) -> None:
        self._timeout_seconds = timeout_seconds

    def run_powershell(self, command: str) -> str:
        """Execute a PowerShell command and return its trimmed stdout."""
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", command],
                capture_output=True,
                text=True,
                timeout=self._timeout_seconds,
                check=False,
            )
        except (FileNotFoundError, OSError) as exc:
            raise CommandError(f"PowerShell is unavailable on this host: {exc}") from exc
        except subprocess.TimeoutExpired as exc:
            raise CommandError(f"Command timed out after {self._timeout_seconds}s") from exc

        if result.returncode != 0:
            raise CommandError(result.stderr.strip() or f"Command exited with code {result.returncode}")

        return result.stdout.strip()

    def run_shell(self, args: list[str]) -> str:
        """Execute a plain command (e.g. `net accounts`) and return its trimmed stdout."""
        try:
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=self._timeout_seconds,
                check=False,
            )
        except (FileNotFoundError, OSError) as exc:
            raise CommandError(f"Command unavailable on this host: {exc}") from exc
        except subprocess.TimeoutExpired as exc:
            raise CommandError(f"Command timed out after {self._timeout_seconds}s") from exc

        if result.returncode != 0:
            raise CommandError(result.stderr.strip() or f"Command exited with code {result.returncode}")

        return result.stdout.strip()
