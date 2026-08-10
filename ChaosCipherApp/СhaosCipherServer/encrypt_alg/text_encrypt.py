# def normalize(x, N):
#     return int(N * (fract(x)))
# def normalize_odd(x, N):
#     v= normalize(x, N)
#     while math.gcd(v, N) != 1:
#         v = (v + 2) % N
#         if v == 0:
#             v = 1
#     return v
# def encrypt_text_chars(content, gen):
#     N = 0x110000
#     B = bytes_per_value(N)
#     result = bytearray()
#     generated_sequence = gen.get_sequence(length=2*len(content))
#     #N = 1114112
#     generated_sequence_norm=[]
#     for i in range(0,len(generated_sequence), 2):
#         normalized_a_i = normalize_odd(generated_sequence[i], N)
#         normalized_b_i=normalize(generated_sequence[i+1], N)
#         generated_sequence_norm.append(normalized_a_i)
#         generated_sequence_norm.append(normalized_b_i)

#     for i in range(len(content)):
#         generated_index = i + i
#         generated_a= generated_sequence_norm[generated_index]
#         generated_b=generated_sequence_norm[generated_index+1]
#         result_i= transform_ch(content[i],generated_a,generated_b, N)
#         result += result_i.to_bytes(B, "big")
#     return base64.b64encode(result).decode("ascii")

# def decrypt_text_chars(cipher_b64: str, gen):
#     try:
#         N = 0x110000
#         B = bytes_per_value(N)
#         raw = base64.b64decode(cipher_b64)
#         n = len(raw) //B
#         result = ""
#         generated_sequence = gen.get_sequence(length=2*n)
#         #N = 1114112
#         generated_sequence_norm=[]
#         for i in range(0, len(generated_sequence), 2):
#             normalazied_a_i = normalize_odd(generated_sequence[i], N)
#             normalazied_b_i = normalize(generated_sequence[i + 1], N)
#             generated_sequence_norm.append(normalazied_a_i)
#             generated_sequence_norm.append(normalazied_b_i)
#
#         for i in range(n):
#             gererated_index = i + i
#             generated_a= generated_sequence_norm[gererated_index]
#             generated_b=generated_sequence_norm[gererated_index+1]
#             elment_i= int.from_bytes(raw[B*i: B*i+B], "big")
#             result_i = transform_ch_back(elment_i, generated_a, generated_b, N)
#             result += chr(int(result_i))
#         return result
#     except Exception as e:
#         raise RuntimeError(f"Помилка дешуфрування тексту. Неправильно введені параметри або формат даних.: {e}") from e

import ast
import base64
import numpy as np
MAX_TEXT_LENGTH = 200_000
_DECRYPT_FACTOR = 5

def is_valid_unicode_scalar(code: int) -> bool:
    return 0 <= code <= 0x10FFFF and not (0xD800 <= code <= 0xDFFF)

def encrypt_text_bytes(content, gen):
    initial_data = content.encode("utf-8")
    generating_sequence_length = len(initial_data)
    generated_sequence = gen.get_sequence(generating_sequence_length)
    generated_sequence_string = b"".join(generated_sequence)
    ciphered_bits = bytes(initial_data[i] ^ generated_sequence_string[i] for i in range(len(initial_data)))
    ciphered_text = f"{ciphered_bits}"
    return ciphered_text
def decrypt_text_bytes(content, gen):
    if not (content.startswith("b'") or content.startswith('b"')):
        raise ValueError(
            "Невірний формат для дешифрування в bytes-режимі. "
            "Очікується рядок виду b'...'"
        )
    try:
        initial_data = ast.literal_eval(content)
    except (ValueError, SyntaxError) as e:
        raise ValueError(
            "Невірний формат шифротексту для bytes-режиму"
        ) from e
    if not isinstance(initial_data, bytes):
        raise ValueError("Невірний формат: очікуються байти (bytes)")
    generating_sequence_length = len(initial_data)
    generated_sequence = gen.get_sequence(generating_sequence_length)
    generated_sequence_string = b"".join(generated_sequence)
    decrypted = bytes(initial_data[i] ^ generated_sequence_string[i] for i in range(len(initial_data)))
    try:
        return decrypted.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError(
            "Помилка дешифрування: результат не є валідним UTF-8. "
            "Перевірте параметри ключа та режим шифрування"
        )
def fract (x):
    return abs(x) %1



def normalize_vec(seq, N):
    return (N * (np.abs(seq) % 1)).astype(np.int64)

def normalize_odd_vec(seq, N):
    v = normalize_vec(seq, N)
    v = v | 1                             
    v[v % 17 == 0] += 2                 
    v[v == 0] = 1                        
    return v

def bytes_per_value(N: int) -> int:
    return ((N - 1).bit_length() + 7) // 8

def transform_ch(ch:str, gen1, gen2, N):
    code = ((gen1*ord(ch)) + gen2) % N
    return code

def transform_ch_back(encrypted_code, gen1, gen2, N):
    gen1_ch = ( encrypted_code - gen2) % N
    invert_gen1=  pow(gen1, -1, N)
    decrypted_code = (gen1_ch * invert_gen1) % N
    return decrypted_code


def encrypt_text_chars(content, gen):
    N = 0x110000
    B = bytes_per_value(N)
    raw_seq = gen.get_sequence(length=2 * len(content))
    seq = np.array(raw_seq, dtype=np.float64)

    a_vals = normalize_odd_vec(seq[0::2], N)   
    b_vals = normalize_vec(seq[1::2], N)
    ord_arr = np.array([ord(c) for c in content], dtype=np.int64)
    codes = (a_vals * ord_arr + b_vals) % N
    result = bytearray(B * len(content))
    for i, code in enumerate(codes):
        result[B*i : B*i+B] = int(code).to_bytes(B, "big")
    return base64.b64encode(result).decode("ascii")


def decrypt_text_chars(cipher_b64: str, gen):
    N = 0x110000
    B = bytes_per_value(N)

    try:
        raw = base64.b64decode(cipher_b64, validate=True)
    except Exception:
        raise ValueError(
            "Невірний формат для дешифрування в chars-режимі. "
            "Очікується base64-рядок"
        )

    if len(raw) % B != 0:
        raise ValueError(
            f"Невірна довжина шифротексту: {len(raw)} байт не кратно {B}"
        )

    try:
        n = len(raw) // B
        raw_seq = gen.get_sequence(length=2 * n)
        seq = np.array(raw_seq, dtype=np.float64)

        a_vals = normalize_odd_vec(seq[0::2], N)
        b_vals = normalize_vec(seq[1::2], N)

        codes = np.array([
            int.from_bytes(raw[B*i : B*i+B], "big") for i in range(n)
        ], dtype=np.int64)

        inv_a = np.array([pow(int(a), -1, N) for a in a_vals], dtype=np.int64)
        decrypted = ((codes - b_vals) % N * inv_a) % N
        chars = []

        for c in decrypted:
            code = int(c)
            if not is_valid_unicode_scalar(code):
                raise ValueError(
                    "Помилка дешифрування: результат містить недопустимі Unicode-символи. "
                    "Перевірте параметри ключа та режим шифрування"                )

            chars.append(chr(code))
        result = "".join(chars)

        return result
    except Exception as e:
        raise RuntimeError(
            f"Помилка дешифрування тексту. Неправильно введені параметри або формат даних.: {e}"
        ) from e


def encrypt_text(content, gen, mode):
    if len(content) == 0:
        raise ValueError("Помилка шифрування! В шифратор тексту передано пустий рядок!")
    if mode == "bytes" and len(content.encode("utf-8")) > MAX_TEXT_LENGTH:
        raise ValueError(
            f"Помилка шифрування! Текст завеликий для bytes-режиму шифрування! Макимальний розмір для шифрування {MAX_TEXT_LENGTH}")
    if mode == "chars" and len(content) > MAX_TEXT_LENGTH:
        raise ValueError(
            f"Помилка шифрування! Текст завеликий для chars-режиму дешифрування! Макимальний розмір для шифрування {MAX_TEXT_LENGTH
            
            }")
    if mode == "bytes":  
        return encrypt_text_bytes(content, gen)
    else:
        enrypted_text = encrypt_text_chars(content, gen)
        return enrypted_text

def decrypt_text(content, gen, mode):
    if len(content) == 0:
        raise ValueError("Помилка дешифрування! В дешифратор тексту передано пустий рядок!")
    if mode == "bytes" and len(content.encode("utf-8")) >  MAX_TEXT_LENGTH*_DECRYPT_FACTOR:
        raise ValueError(f"Помилка дешифрування! Текст завеликий для bytes-режиму дешифруфання! Макимальний розмір для дешифрування {MAX_TEXT_LENGTH*_DECRYPT_FACTOR}")
    if mode == "chars" and len(content) > MAX_TEXT_LENGTH*_DECRYPT_FACTOR:
        raise ValueError(f"Помилка дешифрування!Текст завеликий для chars-режиму дешифрування! Макимальний розмір для дешифрування {MAX_TEXT_LENGTH*_DECRYPT_FACTOR}")
    if mode == "bytes":
        return decrypt_text_bytes(content, gen)
    else:
        decrypted_text = decrypt_text_chars(content, gen)
        return decrypted_text
