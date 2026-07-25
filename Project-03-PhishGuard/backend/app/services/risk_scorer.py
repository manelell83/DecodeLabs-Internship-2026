"""Aggregates indicator hits into a single 0-100 phishing risk score."""

from __future__ import annotations

from dataclasses import dataclass

from app.services.types import IndicatorHit

_LEVEL_THRESHOLDS: tuple[tuple[float, str], ...] = (
    (75.0, "Critical"),
    (50.0, "High"),
    (25.0, "Medium"),
    (0.0, "Low"),
)


@dataclass(frozen=True)
class RiskResult:
    """Final scoring outcome for a scan."""

    score: float
    level: str
    summary: str


class RiskScorer:
    """Converts a list of indicator hits into a bounded risk score and level."""

    def score(self, indicators: list[IndicatorHit]) -> RiskResult:
        raw_total = sum(hit.weight for hit in indicators)
        score = min(100.0, round(raw_total, 1))
        level = self._level_for(score)
        summary = self._summarize(indicators, score, level)
        return RiskResult(score=score, level=level, summary=summary)

    @staticmethod
    def _level_for(score: float) -> str:
        for threshold, level in _LEVEL_THRESHOLDS:
            if score >= threshold:
                return level
        return "Low"

    @staticmethod
    def _summarize(indicators: list[IndicatorHit], score: float, level: str) -> str:
        if not indicators:
            return "No phishing indicators were detected in this email."

        categories = sorted({hit.category.replace("_", " ") for hit in indicators})
        preview = ", ".join(categories[:4])
        more = f" and {len(categories) - 4} more" if len(categories) > 4 else ""
        return (
            f"Detected {len(indicators)} indicator(s) across {len(categories)} categor"
            f"{'y' if len(categories) == 1 else 'ies'} ({preview}{more}), "
            f"resulting in a {level.lower()} risk score of {score}/100."
        )
