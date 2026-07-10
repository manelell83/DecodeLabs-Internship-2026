from __future__ import annotations


def classify_score(score: int) -> str:
    """Convert a numeric score into a human-readable strength label."""
    if score < 25:
        return "Weak"
    if score < 50:
        return "Medium"
    if score < 75:
        return "Strong"
    return "Very Strong"
