from __future__ import annotations

import re
import secrets
import string
from dataclasses import dataclass, field
from pathlib import Path

from core.common_passwords import CommonPasswordRepository
from core.entropy import estimate_entropy
from core.scoring import classify_score


@dataclass(slots=True)
class AnalysisResult:
    """Structured result of password analysis."""

    password: str
    score: int
    entropy: float
    level: str
    checklist: dict[str, bool] = field(default_factory=dict)
    suggestions: list[str] = field(default_factory=list)
    flags: dict[str, bool] = field(default_factory=dict)
    brute_force_time: str = ""
    estimated_guesses: int = 0


class PasswordAnalyzer:
    """Analyze password strength using heuristics and entropy estimation."""

    def __init__(self, common_passwords_path: str | None = None) -> None:
        self.common_passwords_path = common_passwords_path or self._default_common_passwords_path()
        self.common_passwords_repo = CommonPasswordRepository(self.common_passwords_path)

    def analyze(self, password: str) -> AnalysisResult:
        """Return a complete strength evaluation for the supplied password."""
        if not password:
            return AnalysisResult(
                password=password,
                score=0,
                entropy=0.0,
                level="Weak",
                checklist={
                    "minimum_length": False,
                    "uppercase": False,
                    "lowercase": False,
                    "number": False,
                    "special": False,
                    "pattern_free": False,
                    "common_password": False,
                },
                suggestions=["Enter a password to analyze it."],
                flags={
                    "repeated_sequence": False,
                    "contains_year": False,
                    "keyboard_pattern": False,
                    "name_like": False,
                },
            )

        checklist = {
            "minimum_length": len(password) >= 12,
            "uppercase": bool(re.search(r"[A-Z]", password)),
            "lowercase": bool(re.search(r"[a-z]", password)),
            "number": bool(re.search(r"\d", password)),
            "special": bool(re.search(r"[^A-Za-z0-9]", password)),
            "pattern_free": not self._has_repeated_patterns(password),
            "common_password": self._is_common_password(password),
        }

        flags = {
            "repeated_sequence": self._has_repeated_patterns(password),
            "contains_year": bool(re.search(r"19\d\d|20\d\d", password)),
            "keyboard_pattern": self._has_keyboard_pattern(password),
            "name_like": self._contains_name_like_tokens(password),
        }

        entropy = self._estimate_entropy(password)
        score = self._score_password(password, checklist, flags, entropy)
        level = self._classify_score(score)
        suggestions = self._build_suggestions(checklist, flags)
        brute_force_time = self._estimate_bruteforce_time(entropy)
        estimated_guesses = int(2**max(entropy, 0))

        return AnalysisResult(
            password=password,
            score=score,
            entropy=entropy,
            level=level,
            checklist=checklist,
            suggestions=suggestions,
            flags=flags,
            brute_force_time=brute_force_time,
            estimated_guesses=estimated_guesses,
        )

    def _score_password(
        self,
        password: str,
        checklist: dict[str, bool],
        flags: dict[str, bool],
        entropy: float,
    ) -> int:
        score = 0
        score += 15 if checklist["minimum_length"] else 0
        score += 10 if checklist["uppercase"] else 0
        score += 10 if checklist["lowercase"] else 0
        score += 10 if checklist["number"] else 0
        score += 10 if checklist["special"] else 0
        score += 10 if checklist["pattern_free"] else 0
        score += 0 if checklist["common_password"] else 10
        score += min(25, int(entropy / 4))

        if flags["repeated_sequence"]:
            score -= 10
        if flags["contains_year"]:
            score -= 5
        if flags["keyboard_pattern"]:
            score -= 8
        if flags["name_like"]:
            score -= 10

        return max(0, min(100, score))

    def _classify_score(self, score: int) -> str:
        return classify_score(score)

    def _estimate_entropy(self, password: str) -> float:
        return estimate_entropy(password)

    def _build_suggestions(self, checklist: dict[str, bool], flags: dict[str, bool]) -> list[str]:
        suggestions: list[str] = []
        if not checklist["minimum_length"]:
            suggestions.append("Use at least 12 characters.")
        if not checklist["uppercase"]:
            suggestions.append("Add uppercase letters.")
        if not checklist["lowercase"]:
            suggestions.append("Add lowercase letters.")
        if not checklist["number"]:
            suggestions.append("Include numbers.")
        if not checklist["special"]:
            suggestions.append("Add special characters.")
        if not checklist["pattern_free"]:
            suggestions.append("Avoid repeated sequences and predictable structures.")
        if checklist["common_password"]:
            suggestions.append("Avoid common passwords and personal information.")
        if flags["keyboard_pattern"]:
            suggestions.append("Avoid keyboard walks like qwerty or 12345.")
        if flags["contains_year"]:
            suggestions.append("Remove years that can be guessed from personal data.")
        if flags["name_like"]:
            suggestions.append("Avoid names, usernames, or dictionary words.")
        if not suggestions:
            suggestions.append("Your password is already strong and varied.")
        return suggestions

    def _estimate_bruteforce_time(self, entropy: float) -> str:
        guesses_per_second = 1_000_000_000
        seconds = 2**entropy / guesses_per_second
        if seconds < 60:
            return f"~{seconds:.0f} seconds"
        if seconds < 3600:
            return f"~{seconds / 60:.1f} minutes"
        if seconds < 86400:
            return f"~{seconds / 3600:.1f} hours"
        if seconds < 31536000:
            return f"~{seconds / 86400:.1f} days"
        if seconds < 31536000000:
            return f"~{seconds / 31536000:.1f} years"
        return "> 1000 years"

    def _has_repeated_patterns(self, password: str) -> bool:
        if len(password) < 4:
            return False
        for index in range(len(password) - 2):
            if password[index : index + 3] in password[index + 1 :]:
                return True
        return False

    def _has_keyboard_pattern(self, password: str) -> bool:
        keyboard_patterns = ["qwerty", "asdf", "zxcv", "12345", "password", "admin"]
        lowered = password.lower()
        return any(pattern in lowered for pattern in keyboard_patterns)

    def _contains_name_like_tokens(self, password: str) -> bool:
        names = {"admin", "root", "password", "user", "guest", "login"}
        lowered = password.lower()
        return any(name in lowered for name in names)

    def _is_common_password(self, password: str) -> bool:
        return self.common_passwords_repo.is_common(password)

    @staticmethod
    def _default_common_passwords_path() -> str:
        return str(Path(__file__).resolve().parents[1] / "data" / "common_passwords.txt")

    @staticmethod
    def generate_secure_password(length: int = 16) -> str:
        """Generate a strong random password with mixed character classes."""
        if length < 12:
            raise ValueError("Length must be at least 12")

        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
        while True:
            candidate = "".join(secrets.choice(alphabet) for _ in range(length))
            if (
                any(char.islower() for char in candidate)
                and any(char.isupper() for char in candidate)
                and any(char.isdigit() for char in candidate)
                and any(char in "!@#$%^&*()-_=+" for char in candidate)
            ):
                return candidate
