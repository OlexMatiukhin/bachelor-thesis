import struct
import zlib
from io import BytesIO
#import fmt
import numpy as np
import PIL.Image as Image
import math
from .crypto_marker import add_marker, remove_marker

MAGIC =b'FSM1'
HEADER_LEN = 16

#Square image
def get_number_iterations_and_size_by_power(r, H, W, header_len: int=16, channels:int =3):
    maximal_side = max(H, W)
    k = 1
    L = r
    while L < maximal_side:
        k += 1
        L= r ** k
    iterations = k - 1
    squared_area_size= L*L
    area =(H*W)
    padding_pixels= squared_area_size - area
    padding_bytes = padding_pixels * 3
    if ((padding_pixels)<0):
        raise ValueError ("Quadratic matrix is too small")
    if (padding_pixels == 0):
        return iterations,  L, False
    if (padding_bytes >=header_len):
        return iterations,  L, True
    needed_pixels = (header_len + channels -1) // channels
    traget_area = area + needed_pixels
    k = 1
    L = r
    while  (L*L) < traget_area:
        k += 1
        L = r ** k

    iterations=k-1
    return iterations, L, True
def add_element_to_pixels_matrix(side_size, H,W, pixels_matrix):
    number_pixels_heigt = side_size - H
    number_pixels_width = side_size - W
    if number_pixels_heigt < 0 or number_pixels_width < 0:
        raise ("Matrix should be bigger or equal to sides of rectungale")
    if side_size*side_size == H*W:
        return pixels_matrix
    elif side_size > H or side_size>W:
        img_square = np.pad(pixels_matrix,  pad_width=((0,number_pixels_heigt), (0, number_pixels_width), (0, 0)), mode="wrap")
        return img_square
def remove_additional_elements_from_matrix(H,W, redacted_matrix):
    return redacted_matrix[:H, :W]
def square_image(pixels_matrix):
    matrix = np.array([
        [4,3],
        [2,1]], dtype=np.float64)
    r = matrix.shape[0]
    c = matrix.shape[1]
    if(r!=c):
        raise ("Matrix is not square")
    H,W,C = pixels_matrix.shape
    iterations, side_size, header_needed = get_number_iterations_and_size_by_power(r, H, W)
    image_redacted=add_element_to_pixels_matrix(side_size, H, W, pixels_matrix)
    if header_needed:
        image_redacted=embed_header_rgb_in_padding(image_redacted, H, W)
    return  side_size, iterations, image_redacted

def make_header(M: int, N: int) -> bytes:
    payload = MAGIC + struct.pack(">II", M, N)
    crc= zlib.crc32(payload)& 0xffffffff
    return payload + struct.pack(">I", crc)
def parse_header(hdr: bytes):
    if len(hdr) != HEADER_LEN:
        return None
    print(hdr)
    if hdr[:4] != MAGIC:
        return None
    M, N = struct.unpack(">II", hdr[4:12])
    crc_stored = struct.unpack(">I", hdr[12:16])[0]
    crc_calc = zlib.crc32(hdr[:12]) & 0xffffffff
    if crc_stored != crc_calc:
        return None
    return M, N
def embed_header_rgb_in_padding(P_sq: np.ndarray, M: int, N: int) -> np.ndarray:
    hdr= np.frombuffer(make_header(M, N), dtype=np.uint8)
    P_flatten= P_sq.reshape(-1)
    P_flatten[-HEADER_LEN:]= hdr
    P_sq_redeacted = P_flatten.reshape(P_sq.shape)
    return P_sq_redeacted
def extract_header (P_sq: np.ndarray):
    v = P_sq.reshape(-1)
    hdr = v[-HEADER_LEN:].tobytes()
    return parse_header(hdr)



def rank(matrix):
    matrix_1D=matrix.ravel()
    size = len(matrix_1D)
    sorted_idx = np.argsort(matrix_1D, kind="stable")
    rank_1D = np.empty_like(matrix_1D)
    rank_1D[sorted_idx] = np.arange(1, size+1);
    rank_2D = rank_1D.reshape(matrix.shape)
    return rank_2D
def generate_A0(A_prev, A_base):
    A_prev=np.asarray(A_prev, dtype=np.int64)
    A_base=np.asarray(A_base, dtype=np.int64)
    m=A_prev.shape[0]
    m1=A_base.shape[0]
    if(A_prev.shape[0]!=A_prev.shape[1]):
        raise ValueError("Matrix A_prev should be quad")
    if(A_base.shape[0]!=A_base.shape[1]):
        raise ValueError("MatrixA_base should be quad")
    m_new = m1 * m
    factor = (m*m) + 1
    A0 = np.empty((m_new, m_new), dtype=np.int64)
    for i in range(m):
        for j in range(m):
            for p in range(m1):
                for q in range(m1):
                    A0[i*m1+p, j*m1+q] = A_prev[i,j]*factor + A_base[p, q]
    return A0

def get_FSM(base_matrix,iterations):
    A1r = rank(base_matrix)
    A_int = A1r.copy()
    for i in range(iterations):
        A0 = generate_A0(A_int, A1r)
        A_int = rank(A0)
    return A_int
def scrambling(C1, side_size, iterations, PO, base_matrix):
    matrix_size=side_size*side_size
    PO_flatten = PO.reshape(matrix_size, 3)
    sorted_indx = np.argsort(C1, kind="stable")
    fsm=get_FSM(base_matrix, iterations)
    fsm_1= np.asarray(fsm).ravel().astype(np.int64)
    P1 = np.empty_like(PO_flatten)
    for i in range(matrix_size):
        index_S = sorted_indx[i]
        index_F = fsm_1[i]-1
        P1[index_F]= PO_flatten[index_S]
    P1_2d = P1.reshape(side_size, side_size, 3)
    return P1_2d

#Deffusion
def make_T_From_C2 (C2):
    C2 = np.asarray(C2, dtype=np.float64)
    T = (np.ceil(C2*1e5).astype(np.int64) % 256).astype(np.uint8)
    return T
def diffusion(C2,C3, pixels_matrix):
    size = pixels_matrix.size
    if pixels_matrix.dtype != np.uint8:
        raise  ValueError("Matrix should be uint8")
    P0_flatten = pixels_matrix.reshape(-1)
    P1_flatten = np.empty_like(P0_flatten)
    C3_sorted_idx = np.argsort(C3, kind="stable")
    T=make_T_From_C2(C2)
    for i in range(size):
        index_S3 = C3_sorted_idx[i]
        if i==0:
           P1_flatten[i] = T[i] ^ P0_flatten[index_S3]
        else:
            P1_flatten[i] = P1_flatten[i-1] ^ T[i] ^ P0_flatten[index_S3]
    P1 = np.reshape(P1_flatten, (pixels_matrix.shape[0], pixels_matrix.shape[1], 3))
    return P1

def scrambling_decryp(C1, side_size, iterations, P1,  base_matrix):
    matrix_size=side_size*side_size
    P1_flatten = P1.reshape(matrix_size, 3)
    sorted_indx = np.argsort(C1, kind="stable")
    fsm=get_FSM(base_matrix, iterations);
    fsm_1= np.asarray(fsm).ravel().astype(np.int64)
    P0_flatten = np.empty_like(P1_flatten)
    for i in range(matrix_size):
        index_S = sorted_indx[i]
        index_F = fsm_1[i]-1
        P0_flatten[index_S]= P1_flatten[index_F]
    P0_2d = P0_flatten.reshape(side_size, side_size, 3)
    return P0_2d


def diffusion_decrypt(C2,C3, pixels_matrix):
    size = pixels_matrix.size
    if pixels_matrix.dtype != np.uint8:
        raise  ValueError("Matrix should be uint8")
    P1_flatten = pixels_matrix.reshape(-1)
    P0_flatten = np.empty_like(P1_flatten)
    C3_sorted_idx = np.argsort(C3, kind="stable")
    T=make_T_From_C2(C2)
    for i in range(size):
        index_S3 = C3_sorted_idx[i]
        if i==0:
           P0_flatten[index_S3]= P1_flatten[i] ^ T[i]
        else:
            P0_flatten[index_S3] =P1_flatten[i] ^ P1_flatten[i-1] ^ T[i]
    PO = np.reshape(P0_flatten, (pixels_matrix.shape[0], pixels_matrix.shape[1], 3))
    return PO

def log_integer_exponent(N: int, m1: int):
    if N < 1 or m1 < 2:
        return None

    exp = 0
    while N % m1 == 0:
        N //= m1
        exp += 1

    return exp if N == 1 else None


# Encrypt
def encrypt_image(original_file, gen):
    try:
        img = Image.open(BytesIO(original_file))
        img.load()
        img = img.convert("RGB")
        pixels = np.array(img)
        side_size,iterations,redacted_array=square_image(pixels)
        number_element=side_size*side_size
        general_number_element= number_element + 2*(number_element*3)
        C = gen.get_sequence(general_number_element)
        C1= C[:number_element]
        C2 = C[number_element:number_element*4]
        C3 = C[number_element*4:]
        base_matrix_for_scrambling = np.array([
            [4, 3],
            [2, 1]], dtype=np.float64)
        redacted_array_srcambled = scrambling(C1, side_size, iterations, redacted_array, base_matrix_for_scrambling)
        redacted_array_defused = diffusion(C2, C3, redacted_array_srcambled)
        redacted_image = Image.fromarray(redacted_array_defused, mode='RGB')
        buf = BytesIO()
        fmt: str = "PNG"
        redacted_image.save(buf, format=fmt)
        #redacted_immage = buf.getvalue()
        #image_3=Image.fromarray(redacted_array_defused,mode='RGB')
        #image_3.show()
        return add_marker(buf.getvalue(), "")
    except Exception as e:
        raise RuntimeError(f"Помилка при шифруванні зображення: {e}") from e

def decrypt_image(original_file, gen):
    try:
        clean_data, meta = remove_marker(original_file)
        img = Image.open(BytesIO(clean_data))
        img.load()
        img = img.convert("RGB")
        pixels = np.array(img)
        r =pixels.shape[0]
        c=pixels.shape[1]
        if(r!=c):
            raise ValueError("Matrix should be quadratic")

        number_element= r * r
        base_matrix_for_scrambling = np.array([
            [4, 3],
            [2, 1]], dtype=np.float64)
        k=log_integer_exponent(r, base_matrix_for_scrambling.shape[0])
        if(not k):
            raise ValueError("Направильний розмір зображення!")

        iterations = k - 1
        general_number_element = number_element + 2 * (number_element * 3)
        C = gen.get_sequence(general_number_element)
        C1 = C[:number_element]
        C2 = C[number_element:number_element * 4]
        C3 = C[number_element * 4:]
        array_defused_reverese = diffusion_decrypt(C2, C3, pixels)
        descrambled_array = scrambling_decryp(C1, r, iterations, array_defused_reverese, base_matrix_for_scrambling)

        header = extract_header(descrambled_array)
        if header is None:
            redacted_image = Image.fromarray(descrambled_array, mode='RGB')
        else:
            old_matrix_size_H, old_matrix_size_W = header
            cutted_array = remove_additional_elements_from_matrix(old_matrix_size_H, old_matrix_size_W, descrambled_array)
            redacted_image = Image.fromarray(cutted_array, mode='RGB')
        buf = BytesIO()
        fmt: str = "PNG"
        redacted_image.save(buf, format=fmt)
        return buf.getvalue()
    except ValueError:
        raise  ValueError("Помилка дешифрування зображення! Невірний розмір або пошкоджений файл або невірний ключ!")
    except Exception as e:
        raise RuntimeError(f"Помилка дешифрування зображення: {e}") from e


