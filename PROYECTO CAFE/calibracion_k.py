import numpy as np
import pandas as pd

def calibrar_k(archivo_csv, M0=50.0, Me=10.0):
    df = pd.read_csv(archivo_csv)
    t = df['tiempo_h'].values
    M = df['humedad_pct'].values
    
    # Transformación lineal: ln((M - Me) / (M0 - Me)) = -k * t
    y = np.log((M - Me) / (M0 - Me))
    x = t
    
    # Mínimos cuadrados
    k_opt = -np.sum(x * y) / np.sum(x**2)
    
    # Coeficiente de determinación R^2
    y_pred = -k_opt * x
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2 = 1 - (ss_res / ss_tot)
    
    print(f"Constante de secado k calculada: {k_opt:.4f} h^-1")
    print(f"Coeficiente de determinación R^2: {r2:.4f}")
    return k_opt, r2

if __name__ == "__main__":
    calibrar_k("data/datos_secado_campo.csv")
