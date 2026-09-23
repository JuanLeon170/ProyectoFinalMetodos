import math

def ecuacion_secado(t, M, k, Me):
    return -k * (M - Me)

def solucion_analitica(t, M0, k, Me):
    return Me + (M0 - Me) * math.exp(-k * t)

def metodo_euler(M0, t_inicial, t_final, h, k, Me):
    tiempos, humedades = [t_inicial], [M0]
    t, M = t_inicial, M0
    while t < t_final:
        if t + h > t_final: h = t_final - t
        M += h * ecuacion_secado(t, M, k, Me)
        t += h
        tiempos.append(round(t, 4))
        humedades.append(round(M, 4))
    return tiempos, humedades

def metodo_rk4(M0, t_inicial, t_final, h, k, Me):
    tiempos, humedades = [t_inicial], [M0]
    t, M = t_inicial, M0
    while t < t_final:
        if t + h > t_final: h = t_final - t
        k1 = ecuacion_secado(t, M, k, Me)
        k2 = ecuacion_secado(t + 0.5 * h, M + 0.5 * h * k1, k, Me)
        k3 = ecuacion_secado(t + 0.5 * h, M + 0.5 * h * k2, k, Me)
        k4 = ecuacion_secado(t + h, M + h * k3, k, Me)
        M += (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        t += h
        tiempos.append(round(t, 4))
        humedades.append(round(M, 4))
    return tiempos, humedades

def calcular_error_absoluto(humedades_num, humedades_exactas):
    return sum(abs(n - e) for n, e in zip(humedades_num, humedades_exactas)) / len(humedades_num)

def calcular_tiempo_parada(tiempos, humedades, humedad_min=11.0, humedad_max=12.0):
    for t, M in zip(tiempos, humedades):
        if humedad_min <= M <= humedad_max:
            return t, M
    return None, None
