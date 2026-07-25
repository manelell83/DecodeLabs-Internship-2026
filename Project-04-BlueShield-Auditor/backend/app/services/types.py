"""Shared data structures used across audit check services."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Status = Literal["pass", "warning", "fail", "info", "unavailable"]
Severity = Literal["Info", "Low", "Medium", "High", "Critical"]
Source = Literal["real", "simulated"]


@dataclass(frozen=True)
class CheckFinding:
    """The result of one security check (or one facet of a multi-part check)."""

    category: str
    status: Status
    severity: Severity
    description: str
    evidence: str
    recommendation: str
    weight: float
    source: Source
