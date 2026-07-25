"""Aggregates check findings into a single 0-100 security posture score."""

from __future__ import annotations

from dataclasses import dataclass

from app.services.types import CheckFinding

_LEVEL_THRESHOLDS: tuple[tuple[float, str], ...] = (
    (85.0, "Excellent"),
    (70.0, "Good"),
    (50.0, "Fair"),
    (0.0, "Poor"),
)

_PENALIZED_STATUSES = {"warning", "fail"}


@dataclass(frozen=True)
class ScoreResult:
    """Final scoring outcome for an audit run."""

    score: float
    level: str
    summary: str


class AuditScorer:
    """Converts a list of findings into a bounded security score and level."""

    def score(self, findings: list[CheckFinding]) -> ScoreResult:
        deductions = sum(f.weight for f in findings if f.status in _PENALIZED_STATUSES)
        score = max(0.0, round(100.0 - deductions, 1))
        level = self._level_for(score)
        summary = self._summarize(findings, score, level)
        return ScoreResult(score=score, level=level, summary=summary)

    @staticmethod
    def _level_for(score: float) -> str:
        for threshold, level in _LEVEL_THRESHOLDS:
            if score >= threshold:
                return level
        return "Poor"

    @staticmethod
    def _summarize(findings: list[CheckFinding], score: float, level: str) -> str:
        issues = [f for f in findings if f.status in _PENALIZED_STATUSES]
        if not issues:
            return f"No security issues detected. Security score: {score}/100 ({level})."

        categories = sorted({f.category.replace("_", " ") for f in issues})
        preview = ", ".join(categories[:4])
        more = f" and {len(categories) - 4} more" if len(categories) > 4 else ""
        return (
            f"Found {len(issues)} issue(s) across {len(categories)} categor"
            f"{'y' if len(categories) == 1 else 'ies'} ({preview}{more}). "
            f"Security score: {score}/100 ({level})."
        )
