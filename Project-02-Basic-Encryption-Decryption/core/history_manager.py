"""History tracking for encryption and decryption operations."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class HistoryManager:
    """Persist and retrieve operation history in JSON format."""

    def __init__(self, history_path: str | Path | None = None) -> None:
        self.history_path = Path(history_path or "data/history.json")
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.history_path.exists():
            self.history_path.write_text("[]", encoding="utf-8")

    def add_entry(
        self,
        *,
        cipher: str,
        operation: str,
        key: str,
        input_preview: str,
        output_preview: str,
    ) -> None:
        """Append a new operation entry to the history file."""
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "cipher": cipher,
            "operation": operation,
            "key": key,
            "input_preview": input_preview,
            "output_preview": output_preview,
        }

        history = self.read_history()
        history.append(entry)
        self.history_path.write_text(json.dumps(history, indent=2), encoding="utf-8")

    def read_history(self) -> list[dict[str, Any]]:
        """Read all history entries."""
        return json.loads(self.history_path.read_text(encoding="utf-8"))

    def clear_history(self) -> None:
        """Clear all history entries."""
        self.history_path.write_text("[]", encoding="utf-8")
