from __future__ import annotations

from pathlib import Path


class CommonPasswordRepository:
    """Load and query a small list of known weak passwords."""

    def __init__(self, path: str | None = None) -> None:
        self.path = path or self._default_path()
        self.passwords = self._load_passwords()

    def is_common(self, password: str) -> bool:
        return password.lower() in self.passwords

    def _load_passwords(self) -> set[str]:
        if not Path(self.path).exists():
            return set()
        with open(self.path, "r", encoding="utf-8") as handle:
            return {line.strip().lower() for line in handle if line.strip()}

    @staticmethod
    def _default_path() -> str:
        return str(Path(__file__).resolve().parents[1] / "data" / "common_passwords.txt")
