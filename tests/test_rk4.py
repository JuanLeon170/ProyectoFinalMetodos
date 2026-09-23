"""
Pruebas unitarias y análisis comparativo de precisión entre Euler y RK4 vs Solución Analítica.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.metodos_edo import (
    calcular_error_absoluto,
    calcular_tiempo_parada,
    metodo_euler,
    metodo_rk4,
    solucion_analitica,
)


def ejecutar_pruebas():
    M0 = 50.0  # Humedad inicial (%)
    Me = 10.0  # Humedad de equilibrio (%)
    k = 0.12  # Constante de secado (1/h)
    t_fin = 30.0  # Tiempo total (horas)

    print("=========================================================")
    print("      PRUEBAS DE PRECISIÓN Y COMPARATIVA EULER VS RK4    ")
    print("=========================================================\n")

    pasos_h = [2.0, 1.0, 0.5, 0.1]

    for h in pasos_h:
        t_e, M_e = metodo_euler(M0, 0.0, t_fin, h, k, Me)
        t_r, M_r = metodo_rk4(M0, 0.0, t_fin, h, k, Me)

        M_exacta = [solucion_analitica(t, M0, k, Me) for t in t_r]

        error_euler = calcular_error_absoluto(M_e, M_exacta)
        error_rk4 = calcular_error_absoluto(M_r, M_exacta)

        print(f"--- Tamaño de paso h = {h} horas ---")
        print(f"  Error Promedio Euler : {error_euler:.6f}")
        print(f"  Error Promedio RK4   : {error_rk4:.6f}")
        print(f"  Diferencia de Error  : {abs(error_euler - error_rk4):.6f}\n")

    hora_opt, hum_opt = calcular_tiempo_parada(t_r, M_r)
    print("---------------------------------------------------------")
    print("CÁLCULO DE PARADA (Café Pergamino Seco - Objetivo 11%-12%):")
    if hora_opt is not None:
        print(
            f"--> Humedad objetivo alcanzada a las {hora_opt} horas con un {hum_opt}% de humedad."
        )
    else:
        print("--> No se alcanzó la humedad objetivo en el tiempo simulado.")
    print("=========================================================")


if __name__ == "__main__":
    ejecutar_pruebas()
