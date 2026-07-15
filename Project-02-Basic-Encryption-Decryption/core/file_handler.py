"""Utilities for importing and exporting plain text files."""

from __future__ import annotations

from pathlib import Path


class FileHandler:
    """Handle simple text file import/export operations."""

    @staticmethod
    def read_text(path: str | Path) -> str:
        """Read text from a .txt file."""
        file_path = Path(path)
        if file_path.suffix.lower() != ".txt":
            raise ValueError("Only .txt files are supported.")
        return file_path.read_text(encoding="utf-8")

    @staticmethod
    def write_text(path: str | Path, content: str) -> None:
        """Write text to a .txt file."""
        file_path = Path(path)
        if file_path.suffix.lower() != ".txt":
            raise ValueError("Only .txt files are supported.")
        file_path.write_text(content, encoding="utf-8")
