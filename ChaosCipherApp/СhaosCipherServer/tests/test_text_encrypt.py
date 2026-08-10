"""
Рівень 3A — Тести шифрування тексту (encrypt_alg/text_encrypt.py).
"""
import math
import pytest
from generators import ChaosFactory
from encrypt_alg.text_encrypt import (
    encrypt_text, decrypt_text,
    encrypt_text_bytes, decrypt_text_bytes,
    encrypt_text_chars, decrypt_text_chars,
    transform_ch, transform_ch_back,
    bytes_per_value,
)
from conftest import LORENZ_PARAMS, ROSSLER_PARAMS

FACTORY = ChaosFactory()


def _make_gen(params=None, mode="chars", system="lorenz"):
    return FACTORY.create_generator(system, params or LORENZ_PARAMS, mode)


class TestTextRoundtripChars:

    @pytest.mark.parametrize("text", [
        "Hello, World!", "Привіт, світ!", "こんにちは 🌍", "a", "A" * 1000,
    ])
    def test_roundtrip(self, text):
        encrypted = encrypt_text_chars(text, _make_gen())
        decrypted = decrypt_text_chars(encrypted, _make_gen())
        assert decrypted == text




class TestTextRoundtripBytes:

    @pytest.mark.parametrize("text", ["Hello, World!", "Привіт!", "test 123"])
    def test_roundtrip_bits(self, text):
        encrypted = encrypt_text_bytes(text, _make_gen(mode="bytes"))
        decrypted = decrypt_text_bytes(encrypted, _make_gen(mode="bytes"))
        assert decrypted == text


class TestTextMainFunction:

    @pytest.mark.parametrize("mode", ["chars", "bytes"])
    def test_encrypt_decrypt(self, mode):
        text = "Test encrypt_text()"
        encrypted = encrypt_text(text, _make_gen(mode=mode), mode)
        decrypted = decrypt_text(encrypted, _make_gen(mode=mode), mode)
        assert decrypted == text

    def test_different_keys_different_ciphertext(self):
        text = "Same plaintext"
        enc1 = encrypt_text_chars(text, _make_gen(LORENZ_PARAMS))
        enc2 = encrypt_text_chars(text, _make_gen(ROSSLER_PARAMS, system="rossler"))
        assert enc1 != enc2

    def test_wrong_key_fails(self):
        encrypted = encrypt_text_chars("Secret", _make_gen(LORENZ_PARAMS))
        decrypted = decrypt_text_chars(encrypted, _make_gen(ROSSLER_PARAMS, system="rossler"))
        assert decrypted != "Secret"


"""class TestHelperFunctions:
    N = 0x110000

    @pytest.mark.parametrize("x", [0.123, 0.999, 3.14159, 100.5])
    def test_normalize_odd_coprime(self, x):
        assert math.gcd(normalize_odd(x, self.N), self.N) == 1

    def test_transform_roundtrip(self):
        for ch in "AБ🎉":
            a = normalize_odd(1.234, self.N)
            b = normalize(5.678, self.N)
            code = transform_ch(ch, a, b, self.N)
            assert transform_ch_back(code, a, b, self.N) == ord(ch)

    def test_bytes_per_value(self):
        assert bytes_per_value(256) == 1
        assert bytes_per_value(65536) == 2
        assert bytes_per_value(0x110000) == 3

    def test_empty_text_chars(self):
        encrypted = encrypt_text_chars("", _make_gen())
        decrypted = decrypt_text_chars(encrypted, _make_gen())
        assert decrypted == """""
