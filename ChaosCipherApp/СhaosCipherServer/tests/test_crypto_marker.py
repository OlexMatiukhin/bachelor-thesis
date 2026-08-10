"""
Рівень 4 — Тести крипто-маркера (encrypt_alg/crypto_marker.py).
"""
import struct
import time
import pytest
from encrypt_alg.crypto_marker import add_marker, remove_marker, is_marked, MAGIC


class TestMarkerRoundtrip:

    @pytest.mark.parametrize("data", [
        b"Hello, World!",
        b"\x00" * 100,
        bytes(range(256)),
        b"",
    ], ids=["text", "zeros", "all_bytes", "empty"])
    def test_add_remove_roundtrip(self, data):
        marked = add_marker(data, "test.txt")
        restored, meta = remove_marker(marked)
        assert restored == data

    def test_meta_fields(self):
        data = b"test data"
        before = int(time.time())
        marked = add_marker(data, "document.pdf")
        after = int(time.time())
        _, meta = remove_marker(marked)
        assert meta is not None
        assert meta["version"] == 1
        assert meta["original_filename"] == "document.pdf"
        assert before <= meta["timestamp"] <= after

    def test_empty_filename(self):
        data = b"data"
        marked = add_marker(data, "")
        _, meta = remove_marker(marked)
        assert meta["original_filename"] == ""

    def test_long_filename_truncated(self):
        """Ім'я файлу > 255 байт UTF-8 обрізається."""
        long_name = "a" * 300
        data = b"test"
        marked = add_marker(data, long_name)
        restored, meta = remove_marker(marked)
        assert restored == data
        assert len(meta["original_filename"]) <= 255


class TestMarkerDetection:

    def test_is_marked_true(self):
        marked = add_marker(b"data", "file.txt")
        assert is_marked(marked)

    def test_is_marked_false_random_data(self):
        assert not is_marked(b"random data without marker")

    def test_is_marked_false_short_data(self):
        assert not is_marked(b"ab")

    def test_remove_marker_no_marker(self):
        data = b"no marker here"
        restored, meta = remove_marker(data)
        assert restored == data
        assert meta is None


class TestMarkerPosition:

    def test_marker_appended_to_end(self):
        """Маркер додається в кінець файлу, а не на початок."""
        data = b"original data"
        marked = add_marker(data, "")
        # Дані на початку зберігаються як є
        assert marked[:len(data)] == data
        # Маркер в кінці
        assert marked[-4:] != data[-4:]  # останні 4 байти — розмір маркера

    def test_marker_size_field(self):
        """Останні 4 байти містять розмір маркера."""
        data = b"test"
        marked = add_marker(data, "file.txt")
        marker_size = struct.unpack(">I", marked[-4:])[0]
        marker_block = marked[-marker_size:]
        assert marker_block.startswith(MAGIC)
