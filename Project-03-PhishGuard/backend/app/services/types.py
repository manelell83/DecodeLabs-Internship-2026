"""Shared lightweight data structures used across analysis services."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class ParsedEmail:
    """Structured representation of a raw email submission."""

    sender: str | None
    subject: str | None
    body: str
    urls: list[str] = field(default_factory=list)
    domains: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class IndicatorHit:
    """A single suspicious signal detected by an analyzer."""

    category: str
    description: str
    evidence: str
    severity: str
    weight: float


class CategorizedIndicator(Protocol):
    """Structural type for anything exposing a `.category` string (hits or ORM rows)."""

    category: str
