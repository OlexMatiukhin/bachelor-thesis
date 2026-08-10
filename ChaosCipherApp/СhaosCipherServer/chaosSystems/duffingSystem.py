import hashlib
import struct
import numpy as np
import math

def runge_kutta(x, y, t, h, delta, gama, omega=1.0):
    half_h = h / 2
    h_divided_six = h / 6
    kx1 = y
    ky1 = (-delta * y) + x - x**3 + gama * math.cos(omega * t)
    kx2 = y + half_h * ky1
    ky2 = -delta * (y + half_h * ky1) + (x + half_h * kx1) - (x + half_h * kx1)**3 + gama * math.cos(omega * (t + half_h))
    kx3 = y + half_h * ky2
    ky3 = -delta * (y + half_h * ky2) + (x + half_h * kx2) - (x + half_h * kx2)**3 + gama * math.cos(omega * (t + half_h))
    kx4 = y + h * ky3
    ky4 = -delta * (y + h * ky3) + (x + h * kx3) - (x + h * kx3)**3 + gama * math.cos(omega * (t + h))
    x_next = x + h_divided_six * (kx1 + 2 * kx2 + 2 * kx3 + kx4)
    y_next = y + h_divided_six * (ky1 + 2 * ky2 + 2 * ky3 + ky4)
    t_next = t + h
    if not (math.isfinite(x_next) and math.isfinite(y_next) and math.isfinite(t_next)):
        raise OverflowError("Duffing trajectory diverged: non-finite state obtained")

    return x_next, y_next, t_next
def duffing_generator(x, y, t):
    delta = 0.2
    gama = 0.3
    omega = 1.0
    h = 0.001
    result = runge_kutta(x, y, t, h,  delta, gama, omega)
    return result
def logistic_generator(x):
    r = 3.99
    x_next = (r*x)*(1-x)
    return x_next
def get_logistic_duffing_sequence(L:int, logistic_x:float, duffing_x:float, duffing_y:float, duffing_t:float, is_sha256:bool):
    L_recalculated= int(np.ceil(L/32)) if is_sha256 else L
    generated_subsequence = []
    w0 = logistic_x
    x= duffing_x
    y = duffing_y
    t = duffing_t
    T1 = 0.14644660940672627
    T2 = 0.5
    T3 = 0.8535533905932737
    eps = 1e-4
    for i in range(L_recalculated):
        w0 = logistic_generator(w0)
        if not (0.0 < w0 < 1.0):
            raise ValueError("logisticX must be in (0,1)")
        x,y,t = duffing_generator(x, y, t)
        delta = eps * w0
        result = w0 + x + y + t
        if w0 < T1:
            x -= delta
            y -= delta
            t-= delta
        elif w0 < T2:
            x += delta
        elif w0 < T3:
            y += delta
        else:
            t+= delta

        if(is_sha256):
            result_bytes = struct.pack(">d", result)
            digest = hashlib.sha256(result_bytes).digest()
            generated_subsequence.extend([digest[j:j + 1] for j in range(32)])
        else:
            generated_subsequence.append(result)
    return w0, x, y, t, generated_subsequence[:L]

