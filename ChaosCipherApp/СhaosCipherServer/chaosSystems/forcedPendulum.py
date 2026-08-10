import hashlib
import math
import struct
import numpy as np

def runge_kutta(theta, nu, t, h,q, omega, F):
    half_h = (h/2)
    h_divided_six = (h/6)
    k_theta_1 = nu
    k_nu_1 = -q * nu - math.sin(theta) + F * math.cos(omega*t)
    k_theta_2 = nu + half_h *k_nu_1
    k_nu_2 =  -q * (nu+ half_h*k_nu_1) - math.sin((theta+ half_h*k_theta_1)) + F * math.cos(omega*(t + half_h))
    k_theta_3 = nu + half_h *k_nu_2
    k_nu_3 =  -q * (nu+ half_h*k_nu_2) - math.sin((theta+ half_h*k_theta_2)) + F * math.cos(omega*(t + half_h))
    k_theta_4 = nu + h * k_nu_3
    k_nu_4 =  -q * (nu + h * k_nu_3) - math.sin((theta + h*k_theta_3)) + F * math.cos(omega*(t + h))
    k_theta_next = theta + h_divided_six * (k_theta_1 + 2*k_theta_2 + 2*k_theta_3 + k_theta_4)
    k_nu_next = nu + h_divided_six * (k_nu_1 + 2*k_nu_2 + 2*k_nu_3 + k_nu_4)
    t_next = t + h
    return k_theta_next, k_nu_next, t_next

def forced_pendulum_generator(theta, nu, t):
    q = 0.5
    omega = 2/3
    F = 1.2
    h = 0.001
    result = runge_kutta(theta, nu, t, h,q, omega, F)
    return result

def logistic_generator(x):
    r = 3.99
    x_next = (r*x)*(1-x)
    return x_next

def get_logistic_forced_pendulum_sequence(L:int, logistic_x:float, van_der_pol_x:float, van_der_pol_y:float, van_der_pol_t:float, is_sha256:bool):
    L_recalculated= int(np.ceil(L/32)) if is_sha256 else L
    generated_subsequence = []
    w0 = logistic_x
    theta= van_der_pol_x
    nu = van_der_pol_y
    t = van_der_pol_t
    T1 = 0.14644660940672627
    T2 = 0.5
    T3 = 0.8535533905932737
    eps=1e-4
    for i in range(L_recalculated):
        w0 = logistic_generator(w0)
        if not (0.0 < w0 < 1.0):
            raise ValueError("logisticX must be in (0,1)")
        theta, nu, t = forced_pendulum_generator(theta, nu, t)
        result = w0 + theta + nu + t
        delta = eps * w0
        if w0 < T1:
            theta -= delta
            nu -= delta
        elif w0 < T2:
            theta += delta
        elif w0 < T3:
            nu += delta
        else:
            theta += delta
            nu += delta
            t += delta
        if(is_sha256):
            result_bytes = struct.pack(">d", result)
            digest = hashlib.sha256(result_bytes).digest()
            generated_subsequence.extend([digest[j:j + 1] for j in range(32)])
        else:
            generated_subsequence.append(result)
    return w0, theta, nu, t, generated_subsequence[:L]