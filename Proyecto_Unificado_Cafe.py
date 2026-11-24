import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Conectar tus módulos reales del repositorio
sys.path.append(os.path.abspath("src"))
sys.path.append(os.path.abspath("PROYECTO CAFE"))

from metodos_edo import metodo_rk4, metodo_euler, calcular_tiempo_parada
from interpolacion_mermas import (
    interpolacion_lagrange,
    spline_cubico,
    simpson_13,
    calcular_tasa_evaporacion,
    balance_masa,
)

print("\n" + "=" * 72)
print("  SISTEMA INTERACTIVO UNIFICADO - MÉTODOS NUMÉRICOS EN CAFÉ (4 GRUPOS)")
print("=" * 72)
print("Instrucción: Escribe tus datos separados por comas cuando se soliciten.")

# ==============================================================================
# PASO 1: ENTRADA DE DATOS POR CONSOLA PARA TODOS LOS MÓDULOS
# ==============================================================================
# 1. Datos para Balance de Materia (Punto 3)
ton_cereza = float(
    input("\n[Punto 3] Inserte toneladas de café cereza cosechada (ej. 5.0): ")
)

# 2. Datos experimentales de Secado / Beneficio (Punto 4 y Punto 2)
proceso = (
    input("[Punto 4] Tipo de beneficio [Lavado / Honey / Natural]: ")
    .strip()
    .capitalize()
)
if proceso not in ["Lavado", "Honey", "Natural"]:
    proceso = "Lavado"

txt_tiempos = input(
    "[Punto 4 y 2] Inserte tiempos de medición en horas separados por coma\n"
    "              (ej. 0, 6, 12, 18, 24, 30, 36): "
)
txt_humedades = input(
    "[Punto 4 y 2] Inserte humedades medidas (%) correspondientes separadas"
    " por coma\n              (ej. 52.0, 41.0, 32.0, 24.5, 18.5, 14.0, 11.2): "
)

t_exp = np.array([float(x.strip()) for x in txt_tiempos.split(",")], dtype=float)
m_exp = np.array(
    [float(x.strip()) for x in txt_humedades.split(",")], dtype=float
)

if len(t_exp) != len(m_exp) or len(t_exp) < 3:
    raise ValueError(
        "Debe ingresar la misma cantidad de tiempos y humedades (mínimo 3"
        " puntos)."
    )

hora_interp = float(
    input(
        "[Punto 4] Inserte la hora intermedia en la que desea interpolar"
        f" humedad (entre {t_exp[0]} y {t_exp[-1]} h): "
    )
)
me_amb = float(
    input(
        "[Punto 2] Inserte la humedad de equilibrio ambiental Me % (ej. 10.0): "
    )
)

# 3. Datos térmicos para Tueste (Punto 1)
txt_temp_tueste = input(
    "[Punto 1] Inserte temperaturas de tueste (°C) medidas cada 1 min (mínimo"
    " 6 datos)\n          (ej. 185, 125, 118, 132, 148, 163, 176, 187, 196,"
    " 204, 211, 216): "
)
T_tueste = np.array(
    [float(x.strip()) for x in txt_temp_tueste.split(",")], dtype=float
)
if len(T_tueste) < 5:
    raise ValueError("Ingrese al menos 5 mediciones de temperatura de tueste.")

# ==============================================================================
# EJECUCIÓN AUTOMÁTICA EN CASCADA (PUNTO 3 -> PUNTO 4 -> PUNTO 2 -> PUNTO 1)
# ==============================================================================

# --- PUNTO 3: BALANCE DE MATERIA (Ax = b) ---
kg_cereza = ton_cereza * 1000.0
A = np.array(
    [
        [1.0, 1.0, 1.0, 1.0],
        [-4.0, 1.0, 0.0, 0.0],
        [-1.5, 0.0, 1.0, 0.0],
        [-3.5, 0.0, 0.0, 1.0],
    ],
    dtype=float,
)
b = np.array([kg_cereza, 0.0, 0.0, 0.0], dtype=float)
x = np.linalg.solve(A, b)
pergamino_humedo_kg = x[0] * 2.0  # Entra a secado con ~50% de humedad

# --- PUNTO 4: CALIBRACIÓN DE k POR MÍNIMOS CUADRADOS E INTERPOLACIÓN ---
M0 = float(m_exp[0])
# Evitamos logaritmos inválidos si algún dato es menor o igual a Me
y_lin = np.log(np.maximum((m_exp - me_amb) / (M0 - me_amb), 1e-4))
k_opt = float(-np.sum(t_exp * y_lin) / np.sum(t_exp**2))

# Coeficiente R^2 del ajuste lineal de k
y_pred = -k_opt * t_exp
r2_k = float(
    1.0 - (np.sum((y_lin - y_pred) ** 2) / np.sum((y_lin - np.mean(y_lin)) ** 2))
)

# Interpolación en la hora solicitada usando tus funciones
hum_spline = float(spline_cubico(t_exp, m_exp, [hora_interp])[0])
hum_lagrange = float(interpolacion_lagrange(t_exp, m_exp, hora_interp))

# Factor de pérdida en tueste (usa datos cafe.xlsx del Punto 4 si existe)
ruta_excel = os.path.join("punto4_beneficio", "datos cafe.xlsx")
if os.path.exists(ruta_excel):
    df_g4 = pd.read_excel(ruta_excel).dropna(
        subset=["Cafe verde (g)", "Cafe tostado (g)"]
    )
    m_tueste, _ = np.polyfit(
        df_g4["Cafe verde (g)"], df_g4["Cafe tostado (g)"], 1
    )
else:
    m_tueste = 0.85

# --- PUNTO 2: EDO DE SECADO (RK4, EULER Y SIMPSON 1/3) ---
t_sim_max = max(120.0, float(t_exp[-1]) * 1.5)
tiempos, hum_rk4 = metodo_rk4(M0, 0.0, t_sim_max, 0.5, k_opt, me_amb)
_, hum_euler = metodo_euler(M0, 0.0, t_sim_max, 0.5, k_opt, me_amb)

t_parada, m_parada = calcular_tiempo_parada(
    tiempos, hum_rk4, humedad_min=10.8, humedad_max=11.5
)
if t_parada is None:
    t_parada, m_parada = tiempos[-1], hum_rk4[-1]

idx_fin = tiempos.index(t_parada)
t_arr = np.array(tiempos[: idx_fin + 1])
m_arr = np.array(hum_rk4[: idx_fin + 1])
if len(t_arr) % 2 == 0:
    t_arr = t_arr[:-1]
    m_arr = m_arr[:-1]

tasa_evap = calcular_tasa_evaporacion(t_arr, m_arr, pergamino_humedo_kg)
agua_evap_kg = float(simpson_13(t_arr, tasa_evap))
masa_final_cps_kg, merma_pct = balance_masa(pergamino_humedo_kg, agua_evap_kg)
error_euler = abs(hum_euler[idx_fin] - hum_rk4[idx_fin])

# --- PUNTO 1: TUESTE DEL CAFÉ (DIFERENCIAS FINITAS Y CURVATURA K) ---
masa_verde_kg = masa_final_cps_kg * 0.82
masa_tostada_kg = masa_verde_kg * 0.85  # Merma física estándar del 15% en tueste

t_tueste = np.arange(0.0, float(len(T_tueste)), 1.0)
dt = 1.0
dT = np.zeros_like(T_tueste)
d2T = np.zeros_like(T_tueste)

# Diferencias finitas O(h^2) del grupo 1
dT[0] = (-3 * T_tueste[0] + 4 * T_tueste[1] - T_tueste[2]) / (2 * dt)
dT[1:-1] = (T_tueste[2:] - T_tueste[:-2]) / (2 * dt)
dT[-1] = (3 * T_tueste[-1] - 4 * T_tueste[-2] + T_tueste[-3]) / (2 * dt)

d2T[0] = (
    2 * T_tueste[0] - 5 * T_tueste[1] + 4 * T_tueste[2] - T_tueste[3]
) / (dt**2)
d2T[1:-1] = (T_tueste[2:] - 2 * T_tueste[1:-1] + T_tueste[:-2]) / (dt**2)
d2T[-1] = (
    2 * T_tueste[-1] - 5 * T_tueste[-2] + 4 * T_tueste[-3] - T_tueste[-4]
) / (dt**2)

K = np.abs(d2T) / np.power(1.0 + np.power(dT, 2), 1.5)
idx_k_max = int(np.argmax(K))
idx_ror_max = int(np.argmax(dT[2:]) + 2)  # Pico de RoR tras fase de secado

# ==============================================================================
# RESULTADOS CONSOLIDADOS Y GRÁFICAS
# ==============================================================================
print("\n" + "-" * 72)
print("RESULTADOS GENERADOS EN CADENA:")
print("-" * 72)
print(
    f"1) [Punto 3 - Balance Ax=b] Cereza: {kg_cereza:.1f} kg -> Pergamino"
    f" húmedo: {pergamino_humedo_kg:.2f} kg | Pulpa: {x[1]:.2f} kg"
)
print(
    f"2) [Punto 4 - Beneficio {proceso}] k calculada: {k_opt:.5f} h^-1 (R² ="
    f" {r2_k:.4f}) | Humedad en {hora_interp} h -> Spline: {hum_spline:.2f}% |"
    f" Lagrange: {hum_lagrange:.2f}%"
)
print(
    f"3) [Punto 2 - Secado RK4 + Simpson] Tiempo hasta ~11%: {t_parada:.1f} h"
    f" | CPS seco: {masa_final_cps_kg:.2f} kg (Merma: {merma_pct:.2f}% | Error"
    f" Euler: {error_euler:.4f}%)"
)
print(
    f"4) [Punto 1 - Tueste Dif. Finitas] Café verde: {masa_verde_kg:.2f} kg ->"
    f" Tostado final: {masa_tostada_kg:.2f} kg | RoR máx:"
    f" {dT[idx_ror_max]:.2f} °C/min (min {t_tueste[idx_ror_max]:.0f}) |"
    f" Curvatura máx K: {K[idx_k_max]:.5f} en min {t_tueste[idx_k_max]:.0f}"
)
print("=" * 72)

fig, axs = plt.subplots(1, 3, figsize=(16, 4.5))

# Gráfica 1: Balance de Masa
axs[0].bar(
    ["Pergamino Húm.", "Pulpa", "Mucílago", "Agua"],
    [pergamino_humedo_kg, x[1], x[2], x[3]],
    color=["#6F4E37", "#A0522D", "#D2B48C", "#4682B4"],
)
axs[0].set_title("Punto 3: Balance de Materia (kg)")
axs[0].set_ylabel("Masa (kg)")
axs[0].grid(axis="y", linestyle="--", alpha=0.5)

# Gráfica 2: Curva de Secado RK4 vs Datos Reales
axs[1].scatter(
    t_exp, m_exp, color="black", zorder=5, label="Datos Ingresados"
)
axs[1].plot(
    tiempos[: idx_fin + 1],
    hum_rk4[: idx_fin + 1],
    label="Modelo RK4",
    color="#1B9E77",
    linewidth=2,
)
axs[1].plot(
    tiempos[: idx_fin + 1],
    hum_euler[: idx_fin + 1],
    "--",
    label="Euler",
    color="#D95F02",
)
axs[1].axhspan(11, 12, color="green", alpha=0.15, label="Objetivo CPS (11-12%)")
axs[1].set_title(f"Punto 2 y 4: Secado ({proceso})")
axs[1].set_xlabel("Tiempo (horas)")
axs[1].set_ylabel("Humedad (%)")
axs[1].legend()
axs[1].grid(True, linestyle="--", alpha=0.5)

# Gráfica 3: Curvatura Geométrica K(t) en Tueste
axs[2].plot(t_tueste, K, marker="o", color="#D62828", linewidth=2)
axs[2].set_title("Punto 1: Curvatura K(t) en Tueste")
axs[2].set_xlabel("Tiempo de tueste (min)")
axs[2].set_ylabel("Curvatura K(t)")
axs[2].grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.show()