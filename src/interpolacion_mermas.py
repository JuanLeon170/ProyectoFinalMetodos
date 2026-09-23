import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline


def interpolacion_lagrange(x_datos, y_datos, x):
    """
    Estima el valor de y para un punto x utilizando
    interpolación polinómica de Lagrange.
    """
    x_datos = np.asarray(x_datos, dtype=float)
    y_datos = np.asarray(y_datos, dtype=float)

    resultado = 0.0

    for i in range(len(x_datos)):
        termino = y_datos[i]

        for j in range(len(x_datos)):
            if i != j:
                termino *= (x - x_datos[j]) / (x_datos[i] - x_datos[j])

        resultado += termino

    return resultado


def spline_cubico(x_datos, y_datos, x_nuevos):
    """
    Calcula valores interpolados mediante un spline cúbico.
    """
    spline = CubicSpline(x_datos, y_datos)
    return spline(x_nuevos)


def simpson_13(x, y):
    """
    Integra numericamente mediante la regla de Simpson 1/3.

    Los puntos deben estar igualmente espaciados y debe existir
    un numero impar de puntos.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if len(x) < 3:
        raise ValueError("Simpson 1/3 necesita al menos 3 puntos.")

    if len(x) % 2 == 0:
        raise ValueError(
            "Simpson 1/3 necesita un numero impar de puntos."
        )

    pasos = np.diff(x)

    if not np.allclose(pasos, pasos[0]):
        raise ValueError(
            "Los puntos de tiempo deben estar igualmente espaciados."
        )

    h = pasos[0]

    integral = (
        h / 3
        * (
            y[0]
            + y[-1]
            + 4 * np.sum(y[1:-1:2])
            + 2 * np.sum(y[2:-2:2])
        )
    )

    return integral


def calcular_tasa_evaporacion(tiempo_h, humedad_pct, masa_inicial_kg):
    """
    Calcula la tasa de perdida de agua del lote en kg/h.

    Se supone que:
    - la humedad esta expresada en base humeda;
    - la materia seca permanece constante;
    - la masa inicial corresponde al primer dato de humedad.

    Devuelve la tasa positiva de evaporacion.
    """
    tiempo_h = np.asarray(tiempo_h, dtype=float)
    humedad_pct = np.asarray(humedad_pct, dtype=float)

    humedad_inicial = humedad_pct[0] / 100

    materia_seca = masa_inicial_kg * (1 - humedad_inicial)

    masa_total = materia_seca / (1 - humedad_pct / 100)

    agua = masa_total - materia_seca

    tasa_evaporacion = -np.gradient(agua, tiempo_h)

    # Evitamos pequenos valores negativos causados por redondeos.
    tasa_evaporacion = np.maximum(tasa_evaporacion, 0)

    return tasa_evaporacion


def balance_masa(masa_inicial_kg, agua_evaporada_kg):
    """
    Calcula la masa final y la merma porcentual.
    """
    masa_final_kg = masa_inicial_kg - agua_evaporada_kg

    merma_pct = (
        agua_evaporada_kg / masa_inicial_kg
    ) * 100

    return masa_final_kg, merma_pct


def cargar_datos(archivo_csv):
    """
    Carga las mediciones de tiempo y humedad desde el CSV.
    """
    df = pd.read_csv(archivo_csv)

    tiempo = df["tiempo_h"].values
    humedad = df["humedad_pct"].values

    return tiempo, humedad


if __name__ == "__main__":

    archivo = "data/datos_secado_campo.csv"

    tiempo, humedad = cargar_datos(archivo)

    print("=== INTERPOLACION Y ANALISIS DE MERMAS ===")
    print()

    # -------------------------------------------------
    # 1. INTERPOLACION DE HUMEDAD
    # -------------------------------------------------

    hora = 7

    humedad_lagrange = interpolacion_lagrange(
        tiempo,
        humedad,
        hora
    )

    humedad_spline = spline_cubico(
        tiempo,
        humedad,
        [hora]
    )[0]

    print(f"Humedad estimada a las {hora} h:")
    print(f"Lagrange: {humedad_lagrange:.2f} %")
    print(f"Spline cubico: {humedad_spline:.2f} %")
    print()

    # -------------------------------------------------
    # 2. EJEMPLO DE TASA DE EVAPORACION
    # -------------------------------------------------

    # Masa inicial del lote.
    # Este valor puede ser reemplazado por el dato real
    # cuando el grupo lo defina.
    masa_inicial = 50.0

    tasa_evaporacion = calcular_tasa_evaporacion(
        tiempo,
        humedad,
        masa_inicial
    )

    # Para aplicar Simpson 1/3 necesitamos puntos
    # igualmente espaciados.
    tiempo_uniforme = np.arange(0, 25, 2)

    tasa_uniforme = spline_cubico(
        tiempo,
        tasa_evaporacion,
        tiempo_uniforme
    )

    agua_evaporada = simpson_13(
        tiempo_uniforme,
        tasa_uniforme
    )

    print("Agua evaporada estimada:")
    print(f"{agua_evaporada:.2f} kg")
    print()

    # -------------------------------------------------
    # 3. BALANCE DE MASA
    # -------------------------------------------------

    masa_final, merma = balance_masa(
        masa_inicial,
        agua_evaporada
    )

    print("Balance de masa:")
    print(f"Masa inicial: {masa_inicial:.2f} kg")
    print(f"Masa final: {masa_final:.2f} kg")
    print(f"Merma: {merma:.2f} %")