"""Unit tests for AuditScorer."""

from app.services.audit_scorer import AuditScorer
from app.services.types import CheckFinding


def _finding(status: str, weight: float, category: str = "test") -> CheckFinding:
    return CheckFinding(
        category=category,
        status=status,
        severity="Medium",
        description="d",
        evidence="e",
        recommendation="r",
        weight=weight,
        source="real",
    )


def test_no_issues_yields_perfect_score():
    result = AuditScorer().score([_finding("pass", 0.0), _finding("info", 0.0)])
    assert result.score == 100.0
    assert result.level == "Excellent"


def test_score_never_goes_below_zero():
    findings = [_finding("fail", 60.0, category=f"cat{i}") for i in range(5)]
    result = AuditScorer().score(findings)
    assert result.score == 0.0
    assert result.level == "Poor"


def test_moderate_deductions_map_to_fair_level():
    findings = [_finding("warning", 20.0), _finding("fail", 20.0, category="other")]
    result = AuditScorer().score(findings)
    assert result.score == 60.0
    assert result.level == "Fair"


def test_small_deduction_maps_to_good_level():
    result = AuditScorer().score([_finding("warning", 20.0)])
    assert result.score == 80.0
    assert result.level == "Good"
