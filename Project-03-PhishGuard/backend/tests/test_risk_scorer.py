"""Unit tests for RiskScorer."""

from app.services.risk_scorer import RiskScorer
from app.services.types import IndicatorHit


def test_no_indicators_yields_low_risk():
    result = RiskScorer().score([])
    assert result.score == 0.0
    assert result.level == "Low"


def test_score_is_capped_at_100():
    hits = [IndicatorHit("x", "d", "e", "Critical", 40.0) for _ in range(5)]
    result = RiskScorer().score(hits)
    assert result.score == 100.0
    assert result.level == "Critical"


def test_moderate_score_maps_to_medium_level():
    hits = [IndicatorHit("x", "d", "e", "Medium", 30.0)]
    result = RiskScorer().score(hits)
    assert result.level == "Medium"
