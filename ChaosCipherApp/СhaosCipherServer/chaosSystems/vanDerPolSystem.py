import hashlib
import math
import struct
import numpy as np

def runge_kutta(x, y, t, h,   mui, omega0quad, A, omega):
    half_h = (h/2)
    h_divided_six = (h/6)
    kx1 = y
    ky1 = mui * (1 - x**2) * y - omega0quad * x + A*math.cos(omega * t)
    kx2 = y + half_h *ky1
    ky2 = mui * (1 - (x + half_h*kx1)**2) * (y + half_h*ky1) - omega0quad * (x + half_h*kx1) + A*math.cos(omega * (t + half_h))
    kx3 = y + half_h * ky2
    ky3 = mui * (1 - (x + half_h*kx2)**2) * (y + half_h*ky2) - omega0quad * (x + half_h*kx2) + A*math.cos(omega * (t + half_h))
    kx4 = y + h * ky3
    ky4 =  mui * (1 - (x + h*kx3)**2) * (y + h*ky3) - omega0quad * (x + h*kx3) + A*math.cos(omega * (t + h))
    x_next = x + h_divided_six * (kx1 + 2*kx2 + 2*kx3 + kx4)
    y_next = y + h_divided_six * (ky1 + 2*ky2 + 2*ky3 + ky4)
    t_next = t + h
    return x_next, y_next, t_next

def van_der_pol_generator(x, y, t):
    mui = 3.4
    omega0quad = math.pi
    A = 2 * omega0quad
    omega = 0.7
    h = 0.001
    result = runge_kutta(x, y, t, h,  mui, omega0quad, A, omega)
    return result

def logistic_generator(x):
    r = 3.99
    x_next = (r*x)*(1-x)
    return x_next

def get_logistic_van_der_pol_sequence(L:int, logistic_x:float, van_der_pol_x:float, van_der_pol_y:float, van_der_pol_t:float, is_sha256:bool):
    L_recalculated= int(np.ceil(L/32)) if is_sha256 else L
    generated_subsequence = []
    w0 = logistic_x
    x= van_der_pol_x
    y = van_der_pol_y
    t = van_der_pol_t
    T1 = 0.14644660940672627
    T2 = 0.5
    T3 = 0.8535533905932737
    eps = 1e-4
    for i in range(L_recalculated):
        w0 = logistic_generator(w0)
        if not (0.0 < w0 < 1.0):
            raise ValueError("logisticX must be in (0,1)")
        x,y,t = van_der_pol_generator(x, y, t)
        result = w0 + x + y + t
        delta = eps * w0
        if w0 < T1:
            x -= delta
            y -= delta
            t -= delta
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