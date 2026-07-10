from __future__ import annotations

from core.password_analyzer import PasswordAnalyzer


def test_strong_password_scores_highly() -> None:
    analyzer = PasswordAnalyzer()
    result = analyzer.analyze("P@ssw0rd!2026")

    assert result.score >= 80
    assert result.level == "Very Strong"
    assert result.checklist["minimum_length"] is True
    assert result.checklist["uppercase"] is True
    assert result.checklist["number"] is True
    assert result.checklist["special"] is True


def test_weak_password_is_detected() -> None:
    analyzer = PasswordAnalyzer()
    result = analyzer.analyze("password")

    assert result.score < 50
    assert result.level == "Weak"
    assert result.checklist["minimum_length"] is False
    assert result.checklist["uppercase"] is False
    assert result.checklist["common_password"] is True


def test_repeated_patterns_and_years_are_flagged() -> None:
    analyzer = PasswordAnalyzer()
    result = analyzer.analyze("Password2025Password2025")

    assert result.flags["repeated_sequence"] is True
    assert result.flags["contains_year"] is True
