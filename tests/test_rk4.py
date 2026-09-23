import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.metodos_edo import metodo_euler, metodo_rk4, solucion_analitica, calcular_error_absoluto, calcular_tiempo_parada

def ejecutar_pruebas():
    M0, Me, k, t_fin = 50.0, 10.0, 0.12, 30.0
    print("=== PRUEBAS EULER VS RK4 ===")
    for h in [2.0, 1.0, 0.5, 0.1]:
        t_e, M_e = metodo_euler(M0, 0.0, t_fin, h, k, Me)
        t_r, M_r = metodo_rk4(M0, 0.0, t_fin, h, k, Me)
        M_ex = [solucion_analitica(t, M0, k, Me) for t in t_r]
        print(f"h={h} -> Err Euler: {calcular_error_absoluto(M_e, M_ex):.4f} | Err RK4: {calcular_error_absoluto(M_r, M_ex):.4f}")
    
    hora, hum = calcular_tiempo_parada(t_r, M_r)
    print(f"Humedad objetivo (11%-12%) alcanzada a las {hora} h con {hum}%.")

if __name__ == "__main__":
    ejecutar_pruebas()
