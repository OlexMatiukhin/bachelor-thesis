import hashlib
import struct
from fractions import Fraction
import numpy as np
def runge_kutta(x:float, y:float, z:float, h:float, sigma:float, rho:float, beta:float):
    half_h = (h/2)
    h_divided_six = (h/6)
    kx1 = sigma * (y - x)
    ky1 = x * (rho - z) - y
    kz1 = x*y - beta*z
    kx2 = sigma * ((y + half_h*ky1) - (x + half_h*kx1))
    ky2 = (x+half_h*kx1) * (rho - (z+half_h*kz1)) - (y + half_h*ky1)
    kz2 = (x + half_h*kx1) * (y + half_h*ky1) - beta*(z + half_h*kz1)
    kx3= sigma * ((y + half_h * ky2) - (x + half_h * kx2))
    ky3= (x + half_h * kx2) * (rho - (z + half_h * kz2)) - (y + half_h * ky2)
    kz3 = (x + half_h * kx2) * (y + half_h * ky2) - beta*(z + half_h*kz2)
    kx4 = sigma * ((y + h * ky3) - (x + h * kx3))
    ky4= (x + h * kx3) * (rho - (z + h * kz3)) - (y + h * ky3)
    kz4 = (x + h * kx3) * (y + h * ky3) - beta * (z + h * kz3)
    x_next = x + h_divided_six * (kx1 + 2*kx2 + 2*kx3 + kx4)
    y_next = y + h_divided_six * (ky1 + 2*ky2 + 2*ky3 + ky4)
    z_next = z + h_divided_six * (kz1 + 2*kz2 + 2*kz3 + kz4)
    return x_next, y_next, z_next
def lorenz_generator(x, y, z):
    sigma = 10.0
    rho = 28.0
    beta =  float(Fraction(8, 3))
    h = 0.01
    result = runge_kutta(x, y, z, h, sigma, rho, beta)
    return result
def logistic_generator(x):
    r = 3.99
    x_next = (r*x)*(1-x)
    return x_next
def get_logistic_lorenz_sequence(L:int, logistic_x:float, lorenz_x:float, lorenz_y:float, lorenz_z:float, is_sha256:bool):
    L_recalculated= int(np.ceil(L/32)) if is_sha256 else L
    generated_subsequence = []
    w0 = logistic_x
    x= lorenz_x
    y = lorenz_y
    z = lorenz_z
    T1 = 0.14644660940672627
    T2 = 0.5
    T3 = 0.8535533905932737
    eps=1e-4
    for i in range(L_recalculated):
        w0 = logistic_generator(w0)
        if not (0.0 < w0 < 1.0):
            raise ValueError("logisticX must be in (0,1)")
        x,y,z = lorenz_generator(x, y, z)
        result = w0 + x + y + z
        delta = eps * w0
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
            generated_subsequence.extend(([digest[j:j+1] for j in range(32)]))

        else:
            generated_subsequence.append(result)
    return w0, x, y, z, generated_subsequence[:L]







