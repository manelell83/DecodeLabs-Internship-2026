from core.caesar_cipher import CaesarCipher


def test_caesar_encrypt_preserves_case_and_punctuation() -> None:
    cipher = CaesarCipher()
    assert cipher.encrypt("Hello, World! 123", 3) == "Khoor, Zruog! 123"


def test_caesar_decrypt_supports_negative_shift() -> None:
    cipher = CaesarCipher()
    assert cipher.decrypt("Khoor, Zruog! 123", 3) == "Hello, World! 123"


def test_caesar_supports_large_shift() -> None:
    cipher = CaesarCipher()
    assert cipher.encrypt("abc", 35) == "jkl"
