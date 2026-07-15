"""Implementation of the Vigenère cipher."""

from __future__ import annotations


class VigenereCipher:
    """Encrypt and decrypt text using the Vigenère cipher."""

    ALPHABET = "abcdefghijklmnopqrstuvwxyz"

    def encrypt(self, text: str, keyword: str) -> str:
        """Encrypt plaintext with a keyword."""
        return self._transform(text, keyword, encrypt=True)

    def decrypt(self, text: str, keyword: str) -> str:
        """Decrypt ciphertext with a keyword."""
        return self._transform(text, keyword, encrypt=False)

    def _transform(self, text: str, keyword: str, *, encrypt: bool) -> str:
        """Apply the Vigenère transformation while preserving non-letters."""
        keyword = self._normalize_keyword(keyword)
        result: list[str] = []
        keyword_index = 0

        for char in text:
            if char.isalpha():
                shift = self._letter_value(keyword[keyword_index % len(keyword)])
                if not encrypt:
                    shift = -shift
                result.append(self._shift_letter(char, shift))
                keyword_index += 1
            else:
                result.append(char)

        return "".join(result)

    def _normalize_keyword(self, keyword: str) -> str:
        """Normalize the keyword to lowercase letters only."""
        return "".join(char.lower() for char in keyword if char.isalpha())

    def _shift_letter(self, char: str, shift: int) -> str:
        """Shift a single letter preserving case."""
        alphabet = self.ALPHABET if char.islower() else self.ALPHABET.upper()
        index = alphabet.index(char.lower())
        shifted = alphabet[(index + shift) % 26]
        return shifted.upper() if char.isupper() else shifted

    def _letter_value(self, char: str) -> int:
        """Return the alphabet index of a letter."""
        return self.ALPHABET.index(char.lower())
