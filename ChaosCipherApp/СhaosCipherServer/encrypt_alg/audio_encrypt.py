import numpy as np
from .crypto_marker import add_marker, remove_marker
import struct

MAX_AUDIO_SIZE = 100 * 1024 * 1024
 

def split_wav(wav_bytes: bytes) -> tuple[bytes, bytes]:
    i = 12
    while i < len(wav_bytes) - 8:
        chunk_id = wav_bytes[i:i+4]
        chunk_size = struct.unpack_from('<I', wav_bytes, i + 4)[0]
        if chunk_id == b'data':
            header = wav_bytes[:i + 8]
            audio_data = wav_bytes[i + 8: i + 8 + chunk_size]
            return header, audio_data
        i += 8 + chunk_size
    raise ValueError("WAV: блок 'data' не знайдено")



def xor_elements(raw,cipher_sequence):
    result = (np.frombuffer(raw, dtype=np.uint8) ^ np.frombuffer(cipher_sequence, dtype=np.uint8)).tobytes()
    return result

def encrypt_audio(original_file, gen):
    if len(original_file) > MAX_AUDIO_SIZE:
        raise ValueError(f"Файл завеликий ({len(original_file)} байт). "
                         f"Максимум: {MAX_AUDIO_SIZE} байт")
   
    header, audio_data = split_wav(original_file)
    general_number_element = len(audio_data)
    generated_sequence = gen.get_sequence(general_number_element)
    generated_sequence_string = b"".join(generated_sequence)
    encrypted_audio_data = xor_elements(audio_data, generated_sequence_string)
    encrypted_wav = header + encrypted_audio_data
    return add_marker(encrypted_wav, "")
    

def decrypt_audio(original_file, gen):
    clean_data, meta = remove_marker(original_file)
    header, encrypted_data = split_wav(clean_data)
    general_number_element = len(encrypted_data)
    generated_sequence = gen.get_sequence(general_number_element)
    generated_sequence_string = b"".join(generated_sequence)
    decrypted_audio_data = xor_elements(encrypted_data, generated_sequence_string)
    return (header + decrypted_audio_data)







