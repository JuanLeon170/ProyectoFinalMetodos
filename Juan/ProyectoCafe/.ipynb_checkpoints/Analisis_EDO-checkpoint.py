"""
Modulo de Metodos Numericos (EDOs) - Secado de Cafe
Integrante 2: Juan Carlos Leon Ramos
Ecuacion diferencial: dM/dt = -k * (M - Me)
"""

def f_secado(t, M, k, Me):
    """Ecuacion diferencial del secado de cafe."""
    return -k * (M - Me)


def metodo_euler(M0, t_inicial, t_final, h, k, Me):
    """Resolucion mediante el Metodo de Euler (1er Orden)."""
    tiempos = [t_inicial]
    humedades = [M0]
    t, M = t_inicial, M0
    while t < t_final:
        if t + h > t_final:
            h = t_final - t
        M = M + h * f_secado(t, M, k, Me)
        t = t + h
        tiempos.append(round(t, 4))
        humedades.append(round(M, 4))
    return tiempos, humedades


def metodo_rk4(M0, t_inicial, t_final, h, k, Me):
    """Resolucion mediante Runge-Kutta de 4º Orden (RK4) sin librerias de EDOs."""
    tiempos = [t_inicial]
    humedades = [M0]
    t, M = t_inicial, M0
    while t < t_final:
        if t + h > t_final:
            h = t_final - t
        k1 = f_secado(t, M, k, Me)
        k2 = f_secado(t + 0.5 * h, M + 0.5 * h * k1, k, Me)
        k3 = f_secado(t + 0.5 * h, M + 0.5 * h * k2, k, Me)
        k4 = f_secado(t + h, M + h * k3, k, Me)
        M = M + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        t = t + h
        tiempos.append(round(t, 4))
        humedades.append(round(M, 4))
    return tiempos, humedades


def calcular_tiempo_parada(tiempos, humedades, humedad_min=11.0, humedad_max=12.0):
    """Identifica la hora en que se alcanza la humedad objetivo (11% - 12%)."""
    for t, M in zip(tiempos, humedades):
        if humedad_min <= M <= humedad_max:
            return t, M
    return None, None


if __name__ == "__main__":
    # Parametros iniciales de prueba
    M0 = 50.0   # Humedad inicial (%)
    Me = 10.0   # Humedad de equilibrio (%)
    k = 0.15    # Constante de secado
    h = 1.0     # Paso de tiempo (horas)
    t_fin = 24.0

    t_e, M_e = metodo_euler(M0, 0.0, t_fin, h, k, Me)
    t_r, M_r = metodo_rk4(M0, 0.0, t_fin, h, k, Me)
    hora_opt, hum_opt = calcular_tiempo_parada(t_r, M_r)

    print("=== SIMULACION DE SECADO DE CAFE (EDOs) ===")
    print(f"Humedad final alcanzada con RK4: {M_r[-1]}%")
    if hora_opt is not None:
        print(f"Zona objetivo (11%-12%) alcanzada en la hora: {hora_opt} h con {hum_opt}% de humedad.")
    else:
        print("No se alcanzo el rango objetivo en el tiempo simulado.")