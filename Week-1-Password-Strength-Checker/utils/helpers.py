from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def export_analysis(payload: dict[str, Any], destination: str) -> Path:
    """Export analysis payload to JSON."""
    path = Path(destination)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
    return path
