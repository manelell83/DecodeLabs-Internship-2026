"""Implementation of the Caesar cipher."""

from __future__ import annotations

from typing import Final


class CaesarCipher:
    """Encrypt and decrypt text using the Caesar cipher."""

    LOWER_CASE: Final[str] = "abcdefghijklmnopqrstuvwxyz"
    UPPER_CASE: Final[str] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def encrypt(self, text: str, shift: int) -> str:
        """Encrypt plaintext using a given shift."""
        return self._transform(text, shift)

    def decrypt(self, text: str, shift: int) -> str:
        """Decrypt ciphertext using a given shift."""
        return self._transform(text, -shift)

    def _transform(self, text: str, shift: int) -> str:
        """Apply the shift to each character while preserving non-letters."""
        normalized_shift = shift % 26
        result: list[str] = []

        for char in text:
            if char.islower():
                index = self.LOWER_CASE.index(char)
                result.append(self.LOWER_CASE[(index + normalized_shift) % 26])
            elif char.isupper():
                index = self.UPPER_CASE.index(char)
                result.append(self.UPPER_CASE[(index + normalized_shift) % 26])
            else:
                result.append(char)

        return "".join(result)
