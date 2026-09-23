"""
Módulo de Métodos Numéricos (EDOs) - Secado de Café
Integrante 2: Programador del Algoritmo Numérico (Juan Carlos León Ramos)
Ecuación diferencial: dM/dt = -k * (M - Me)
"""

import math


def ecuacion_secado(t, M, k, Me):
    """Ecuación diferencial del secado de café: dM/dt = -k*(M - Me)."""
    return -k * (M - Me)


def solucion_analitica(t, M0, k, Me):
    """Solución exacta de la EDO: M(t) = Me + (M0 - Me)*exp(-k*t)."""
    return Me + (M0 - Me) * math.exp(-k * t)


def metodo_euler(M0, t_inicial, t_final, h, k, Me):
    """Método de Euler (1er Orden) para resolver dM/dt = -k*(M - Me)."""
    tiempos = [t_inicial]
    humedades = [M0]
    t, M = t_inicial, M0

    while t < t_final:
        if t + h > t_final:
            h = t_final - t
        M = M + h * ecuacion_secado(t, M, k, Me)
        t = t + h
        tiempos.append(round(t, 4))
        humedades.append(round(M, 4))

    return tiempos, humedades


def metodo_rk4(M0, t_inicial, t_final, h, k, Me):
    """Método de Runge-Kutta de 4º Orden (RK4) sin librerías automáticas de EDOs."""
    tiempos = [t_inicial]
    humedades = [M0]
    t, M = t_inicial, M0

    while t < t_final:
        if t + h > t_final:
            h = t_final - t

        k1 = ecuacion_secado(t, M, k, Me)
        k2 = ecuacion_secado(t + 0.5 * h, M + 0.5 * h * k1, k, Me)
        k3 = ecuacion_secado(t + 0.5 * h, M + 0.5 * h * k2, k, Me)
        k4 = ecuacion_secado(t + h, M + h * k3, k, Me)

        M = M + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        t = t + h

        tiempos.append(round(t, 4))
        humedades.append(round(M, 4))

    return tiempos, humedades


def calcular_error_absoluto(humedades_num, humedades_exactas):
    """Calcula el error absoluto promedio entre la solución numérica y la analítica."""
    errores = [abs(num - ex) for num, ex in zip(humedades_num, humedades_exactas)]
    return sum(errores) / len(errores)


def calcular_tiempo_parada(tiempos, humedades, humedad_min=11.0, humedad_max=12.0):
    """Identifica la hora exacta en que se alcanza la humedad objetivo (11% al 12% - Café Pergamino Seco)."""
    for t, M in zip(tiempos, humedades):
        if humedad_min <= M <= humedad_max:
            return t, M
    return None, None
