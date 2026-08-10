import math
import hashlib
import struct
import time
from dataclasses import dataclass
from fractions import Fraction
from collections import Counter
import numpy as np
def f_x(m0,m1,x):
    return m1*x + 0.5*(m0-m1)*(abs(x+1)-abs(x-1))
def runge_kutta(x, y, z, h, alpha, beta, m0,m1):
    half_h = (h/2)
    h_divided_six = (h/6)
    kx1 = alpha * (y - x- f_x(m0,m1,x))
    ky1 = x -y + z
    kz1 = -beta *y
    kx2 = alpha * ((y + half_h*ky1) - (x + half_h *kx1) - f_x(m0,m1, x + half_h * kx1))
    ky2 = (x+half_h*kx1) - (y + half_h*ky1) + (z + half_h*kz1)
    kz2 = -beta * (y + half_h*ky1)

    kx3 = alpha * ((y + half_h*ky2) - (x + half_h *kx2) - f_x(m0,m1,  x + half_h * kx2))
    ky3 = (x+half_h*kx2) - (y + half_h*ky2) + (z + half_h*kz2)
    kz3 = -beta * (y + half_h*ky2)
    kx4 = alpha * ((y + h*ky3) - (x + h *kx3) - f_x(m0,m1, x + h * kx3))
    ky4 = (x+h*kx3) - (y + h*ky3) + (z + h*kz3)
    kz4 = -beta * (y + h*ky3)
    x_next = x + h_divided_six * (kx1 + 2*kx2 + 2*kx3 + kx4)
    y_next = y + h_divided_six * (ky1 + 2*ky2 + 2*ky3 + ky4)
    z_next = z + h_divided_six * (kz1 + 2*kz2 + 2*kz3 + kz4)
    return x_next, y_next, z_next
def chua_generator(x, y, z):
    alpha = 15.6
    beta = 28
    m0 = - float(Fraction(8, 7))
    m1 = - float(Fraction(5, 7))

    h = 0.001
    result = runge_kutta(x, y, z, h, alpha, beta, m0,m1)
    return result
def logistic_generator(x):
    r = 3.99
    x_next = (r*x)*(1-x)
    return x_next
def get_logistic_chua_sequence(L:int, logistic_x:float, chua_x:float, chua_y:float, chua_z:float, is_sha256:bool):
    L_recalculated= int(np.ceil(L/32)) if is_sha256 else L
    generated_subsequence = []
    w0 = logistic_x
    x= chua_x
    y = chua_y
    z = chua_z
    T1 = 0.14644660940672627
    T2 = 0.5
    T3 = 0.8535533905932737
    eps=1e-4
    for i in range(L_recalculated):
        w0 = logistic_generator(w0)
        if not (0.0 < w0 < 1.0):
            raise ValueError("logisticX must be in (0,1)")
        x,y,z = chua_generator(x, y, z)
        result = w0 + x + y + z
        delta = eps * (1-w0)
        if w0 < T1:
            x -= delta
            y -= delta
            z -= delta
        elif w0 < T2:
            x += delta
        elif w0 < T3:
            y += delta
        else:
            z += delta

        if(is_sha256):
            result_bytes = struct.pack(">d", result)
            digest = hashlib.sha256(result_bytes).digest()
            generated_subsequence.extend([digest[j:j + 1] for j in range(32)])
        else:
            generated_subsequence.append(result)
    return w0,x, y, z, generated_subsequence[:L]





