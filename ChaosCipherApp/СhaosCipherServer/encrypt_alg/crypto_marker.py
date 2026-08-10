# crypto_marker.py
"""import struct
import time

MAGIC = b"CHAOSENC"
VERSION = 1
HEADER_SIZE = 8 + 1 + 1 + 8


def add_marker(data: bytes, original_filename: str = "") -> bytes:
    name_bytes = original_filename.encode("utf-8")[:255]
    header = (
        MAGIC
        + struct.pack("B", VERSION)
        + struct.pack("B", len(name_bytes))
        + struct.pack(">Q", int(time.time()))
        + name_bytes
    )
    return header + data


def remove_marker(data: bytes) -> tuple[bytes, dict | None]:
    if not data.startswith(MAGIC):
        return data, None  # маркера немає — файл не зашифровано цією системою

    offset = len(MAGIC)
    version   = data[offset];     offset += 1
    name_len  = data[offset];     offset += 1
    timestamp = struct.unpack(">Q", data[offset:offset+8])[0]; offset += 8
    filename  = data[offset:offset+name_len].decode("utf-8", errors="replace")
    offset   += name_len
    meta = {"version": version, "timestamp": timestamp, "original_filename": filename}
    return data[offset:], meta



def is_marked(data: bytes) -> bool:
    return data[:len(MAGIC)] == MAGIC"""
# crypto_marker.py
import struct
import time

MAGIC = b"CHAOSENC"
VERSION = 1

def add_marker(data: bytes, original_filename: str = "") -> bytes:
    name_bytes = original_filename.encode("utf-8")[:255]
    marker_size = len(MAGIC) + 1 + 1 + 8 + len(name_bytes) + 4  

    marker = (
        MAGIC
        + struct.pack("B", VERSION)
        + struct.pack("B", len(name_bytes))
        + struct.pack(">Q", int(time.time()))
        + name_bytes
        + struct.pack(">I", marker_size)  
    )
    return data + marker


def remove_marker(data: bytes) -> tuple[bytes, dict | None]:
    if len(data) < 4:
        return data, None


    marker_size = struct.unpack(">I", data[-4:])[0]

    if marker_size > len(data) or marker_size < len(MAGIC) + 1 + 1 + 8 + 4:
        return data, None  

    marker_block = data[-marker_size:]

    if not marker_block.startswith(MAGIC):
        return data, None  
    offset = len(MAGIC)
    version   = marker_block[offset];     offset += 1
    name_len  = marker_block[offset];     offset += 1
    timestamp = struct.unpack(">Q", marker_block[offset:offset+8])[0]; offset += 8
    filename  = marker_block[offset:offset+name_len].decode("utf-8", errors="replace")
    meta = {"version": version, "timestamp": timestamp, "original_filename": filename}
    return data[:-marker_size], meta


def is_marked(data: bytes) -> bool:
    if len(data) < 4:
        return False
    marker_size = struct.unpack(">I", data[-4:])[0]
    if marker_size > len(data):
        return False
    return True