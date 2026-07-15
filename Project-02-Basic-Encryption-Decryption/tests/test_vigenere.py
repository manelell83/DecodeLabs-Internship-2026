from core.vigenere_cipher import VigenereCipher


def test_vigenere_encrypt() -> None:
    cipher = VigenereCipher()
    assert cipher.encrypt("hello world", "key") == "rijvs uyvjn"


def test_vigenere_decrypt() -> None:
    cipher = VigenereCipher()
    assert cipher.decrypt("rijvs uyvjn", "key") == "hello world"


def test_vigenere_preserves_non_letters() -> None:
    cipher = VigenereCipher()
    assert cipher.encrypt("hello, world!", "key") == "rijvs, uyvjn!"
