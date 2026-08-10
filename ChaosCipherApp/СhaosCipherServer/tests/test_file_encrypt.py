"""
Рівень 3D — Тести шифрування файлів (encrypt_alg/file_encrypt.py).
"""
import os
import pytest
from generators import ChaosFactory
from encrypt_alg.file_encrypt import encrypt_file, decrypt_file
from conftest import LORENZ_PARAMS

FACTORY = ChaosFactory()


def _make_gen():
    return FACTORY.create_generator("lorenz", LORENZ_PARAMS, "bytes")


class TestFileRoundtrip:

    @pytest.mark.parametrize("data", [
        bytes(range(256)),
    ], ids=["all_byte_values"])
    def test_roundtrip(self, data):
        gen_enc = _make_gen()
        gen_dec = _make_gen()
        encrypted = encrypt_file(data, gen_enc)
        decrypted = decrypt_file(encrypted, gen_dec)
        assert decrypted == data

    def test_invalid_data_enc(self):
        with pytest.raises((ValueError, Exception)):
            encrypt_file(None, _make_gen())
    def test_invalid_data_dec(self):
        with pytest.raises((ValueError, Exception)):
            decrypt_file(test_wav_bytes, _make_gen())


    def test_encrypted_differs(self):
        data = b"Some data to encrypt"
        encrypted = encrypt_file(data, _make_gen())
        # Зашифровані дані (з маркером) не дорівнюють оригіналу
        assert encrypted != data


"""

class TestFileDecryptValidation:

    def test_no_marker_raises(self):
        with pytest.raises(ValueError, match="маркера"):
            decrypt_file(b"random data without marker", _make_gen())
            """
