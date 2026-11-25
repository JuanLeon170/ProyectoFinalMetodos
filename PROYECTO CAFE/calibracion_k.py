import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def calibrar_modelos(archivo_csv, Me=10.0):
    """
    Calibra los modelos de Thin-Layer (Lewis) y Henderson-Pabis mediante
    Mínimos Cuadrados Ordinarios y evalúa su ajuste con R^2.
    """
    # 1. Validación de ruta (busca en la carpeta actual o en data/)
    if not os.path.exists(archivo_csv):
        ruta_alternativa = os.path.join("data", os.path.basename(archivo_csv))
        if os.path.exists(ruta_alternativa):
            archivo_csv = ruta_alternativa
        else:
            raise FileNotFoundError(f"No se encontró el archivo: {archivo_csv}")

    df = pd.read_csv(archivo_csv)
    t_raw = df["tiempo_h"].values
    M_raw = df["humedad_pct"].values

    # Humedad inicial tomada automáticamente del primer registro
    M0 = float(M_raw[0])

    # 2. Filtro de seguridad: evitar M <= Me para que ln(Y) no falle
    mask = M_raw > Me
    x = t_raw[mask]
    M = M_raw[mask]

    # Transformación lineal: y = ln((M - Me) / (M0 - Me))
    Y = (M - Me) / (M0 - Me)
    y = np.log(Y)

    # =========================================================================
    # MODELO 1: Thin-Layer / Lewis (y = -k * x) -> Recta forzada al origen
    # =========================================================================
    k_tl = -np.sum(x * y) / np.sum(x ** 2)
    y_pred_tl = -k_tl * x

    ss_res_tl = np.sum((y - y_pred_tl) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2_tl = 1 - (ss_res_tl / ss_tot)

    # =========================================================================
    # MODELO 2: Henderson-Pabis (y = ln(a) - k * x) -> Ecuaciones Normales 2x2
    # =========================================================================
    n = len(x)
    # Sistema matricial de Gauss: [n, sum(x); sum(x), sum(x^2)] * [b; m] = [sum(y); sum(x*y)]
    A = np.array([
        [n, np.sum(x)],
        [np.sum(x), np.sum(x ** 2)]
    ])
    B = np.array([np.sum(y), np.sum(x * y)])
    b_hp, m_hp = np.linalg.solve(A, B)

    k_hp = -m_hp
    a_hp = np.exp(b_hp)
    y_pred_hp = b_hp + m_hp * x

    ss_res_hp = np.sum((y - y_pred_hp) ** 2)
    r2_hp = 1 - (ss_res_hp / ss_tot)

    # =========================================================================
    # REPORTE EN CONSOLA
    # =========================================================================
    print("=" * 55)
    print("   CALIBRACIÓN DEL MODELO DE SECADO DE CAFÉ (MCO)")
    print("=" * 55)
    print(f"Humedad Inicial (M0): {M0:.2f}% | Humedad Equilibrio (Me): {Me:.2f}%\n")

    print("1. Modelo Thin-Layer (Lewis): Y = exp(-k * t)")
    print(f"   -> Constante k: {k_tl:.5f} h^-1")
    print(f"   -> Ajuste R^2:  {r2_tl:.5f} ({r2_tl*100:.2f}%)\n")

    print("2. Modelo Henderson-Pabis:    Y = a * exp(-k * t)")
    print(f"   -> Constante k: {k_hp:.5f} h^-1")
    print(f"   -> Factor a:    {a_hp:.5f}")
    print(f"   -> Ajuste R^2:  {r2_hp:.5f} ({r2_hp*100:.2f}%)")
    print("=" * 55)

    # =========================================================================
    # GENERACIÓN DE GRÁFICAS COMPARATIVAS
    # =========================================================================
    t_continuo = np.linspace(0, max(x), 100)
    M_pred_tl = Me + (M0 - Me) * np.exp(-k_tl * t_continuo)
    M_pred_hp = Me + (M0 - Me) * a_hp * np.exp(-k_hp * t_continuo)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Subgráfica 1: Espacio Linealizado
    ax1.scatter(x, y, color="black", label="Datos experimentales ln(Y)", zorder=3)
    ax1.plot(x, y_pred_tl, "--", color="tab:blue", label=f"Thin-Layer (R² = {r2_tl:.4f})")
    ax1.plot(x, y_pred_hp, "-.", color="tab:orange", label=f"Henderson-Pabis (R² = {r2_hp:.4f})")
    ax1.set_title("Linealización Logarítmica: ln(Y) vs Tiempo")
    ax1.set_xlabel("Tiempo t (horas)")
    ax1.set_ylabel("ln(Y)")
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # Subgráfica 2: Espacio Físico Real
    ax2.scatter(x, M, color="tab:green", label="Humedad medida M (%)", zorder=3)
    ax2.plot(t_continuo, M_pred_tl, "-", color="tab:blue", linewidth=2, label="Thin-Layer M(t)")
    ax2.plot(t_continuo, M_pred_hp, "--", color="tab:orange", linewidth=2, label="Henderson-Pabis M(t)")
    ax2.axhline(Me, color="gray", linestyle=":", label=f"Equilibrio Me = {Me}%")
    ax2.set_title("Curva Física de Secado de Café")
    ax2.set_xlabel("Tiempo t (horas)")
    ax2.set_ylabel("Contenido de Humedad M (%)")
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    plt.savefig("calibracion_resultado.png", dpi=150)
    plt.show()

    return {
        "k_thin_layer": k_tl,
        "r2_thin_layer": r2_tl,
        "k_henderson_pabis": k_hp,
        "a_henderson_pabis": a_hp,
        "r2_henderson_pabis": r2_hp
    }


if __name__ == "__main__":
    calibrar_modelos("datos_secado_campo.csv", Me=10.0)
