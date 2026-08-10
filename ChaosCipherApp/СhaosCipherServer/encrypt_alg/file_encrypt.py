from typing import Iterator
from .crypto_marker import add_marker, remove_marker
import numpy as np

MAX_FILE_SIZE = 100 * 1024 * 1024
MIN_FILE_SIZE = 1
CHUNK_SIZE = 64 * 1024


def encrypt_file(original_file, gen, filename: str = ""):    
    if len(original_file) < MIN_FILE_SIZE:
        raise ValueError("Файл порожній — нічого шифрувати")
    if len(original_file) > MAX_FILE_SIZE:
        raise ValueError(f"Файл завеликий ({len(original_file)} байт). "
                         f"Максимум: {MAX_FILE_SIZE} байт")
    general_number_element = len(original_file)
    generated_sequence = gen.get_sequence(general_number_element)
    key = np.frombuffer(b"".join(generated_sequence), dtype=np.uint8)
    data = np.frombuffer(original_file, dtype=np.uint8)
    encrypted_file = (data ^ key).tobytes()
    encrypted_file_with_marker=add_marker(encrypted_file, filename)
    return encrypted_file_with_marker

def decrypt_file(original_file, gen):
    clean_data, meta = remove_marker(original_file)
    if meta is None:
        raise ValueError("Файл не зашифровано")
    if len(clean_data) < MIN_FILE_SIZE:
        raise ValueError("Файл порожній — нічого розшифровувати")
    if len(clean_data) > MAX_FILE_SIZE:
        raise ValueError(f"Файл завеликий ({len(clean_data)} байт). "
                         f"Максимум: {MAX_FILE_SIZE} байт")
    general_number_element = len(clean_data)
    generated_sequence = gen.get_sequence(general_number_element)
    key = np.frombuffer(b"".join(generated_sequence), dtype=np.uint8)
    data = np.frombuffer(clean_data, dtype=np.uint8)
    decrypted_file = (data ^ key).tobytes()
    decrypted_file_with_marker=add_marker(decrypted_file, "")
    return decrypted_file_with_marker



def encrypt_file_stream(data_stream: Iterator[bytes], gen, filename: str = "") -> Iterator[bytes]:
    for chunk in data_stream:
        seq = gen.get_sequence(len(chunk))
        key = b"".join(seq)
        encrypted = (
            np.frombuffer(chunk, dtype=np.uint8)
            ^ np.frombuffer(key, dtype=np.uint8)
        ).tobytes()
        yield encrypted
    marker = add_marker(b"", filename)
    yield marker

def decrypt_file_stream(data_stream: Iterator[bytes], gen) -> Iterator[bytes]:
    full_data = b"".join(data_stream)
    clean_data, meta = remove_marker(full_data)
    if meta is None:
        raise ValueError("Файл не зашифровано")
    for i in range(0, len(clean_data), CHUNK_SIZE):
        chunk = clean_data[i:i + CHUNK_SIZE]
        seq = gen.get_sequence(len(chunk))
        key = b"".join(seq)
        decrypted = (
            np.frombuffer(chunk, dtype=np.uint8)
            ^ np.frombuffer(key, dtype=np.uint8)
        ).tobytes()
        yield decrypted

