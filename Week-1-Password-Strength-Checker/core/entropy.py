from __future__ import annotations

import math
import re


def estimate_entropy(password: str) -> float:
    """Estimate password entropy based on character classes and length."""
    charset_size = 0
    if re.search(r"[a-z]", password):
        charset_size += 26
    if re.search(r"[A-Z]", password):
        charset_size += 26
    if re.search(r"\d", password):
        charset_size += 10
    if re.search(r"[^A-Za-z0-9]", password):
        charset_size += 32
    if charset_size == 0:
        return 0.0
    return len(password) * math.log2(charset_size)
