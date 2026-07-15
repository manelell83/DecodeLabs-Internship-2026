"""Validation helpers for user input."""

from __future__ import annotations


class ValidationError(ValueError):
    """Raised when the user provides invalid input."""


def validate_text(text: str) -> str:
    """Ensure the input text is not empty."""
    if not text.strip():
        raise ValidationError("Text input cannot be empty.")
    return text


def validate_shift(shift: str) -> int:
    """Validate that the shift is an integer."""
    try:
        value = int(shift)
    except ValueError as exc:
        raise ValidationError("Shift must be a valid integer.") from exc
    return value


def validate_keyword(keyword: str) -> str:
    """Ensure a Vigenère keyword contains at least one letter."""
    if not keyword or not any(char.isalpha() for char in keyword):
        raise ValidationError("Keyword must include at least one letter.")
    return keyword
