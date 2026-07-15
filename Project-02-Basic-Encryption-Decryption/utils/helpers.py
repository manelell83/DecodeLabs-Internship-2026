"""Helper utilities for UI and formatting."""

from __future__ import annotations


def truncate(text: str, limit: int = 40) -> str:
    """Return a shortened preview for history display."""
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."
