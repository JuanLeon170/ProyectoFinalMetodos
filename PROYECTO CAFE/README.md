# ProyectoFinalMetodos
# Mermas de secado del café 
# Laura Sofia Bolivar Jimenez
## 1. Modelamiento fisico y calibracion de datos
Constituye la base física y numérica para simular el proceso de secado del café pergamino lavado. En la poscosecha, controlar la velocidad con la que el grano pierde agua resulta indispensable para evitar tanto la proliferación de hongos por exceso de humedad ($M > 12\%$) como la cristalización y fractura física por sobre-secado ($M < 10\%$). Por consiguiente, este desarrollo transforma mediciones experimentales de campo (`datos_secado_campo.csv`) en constantes cinéticas calibradas mediante el algoritmo `calibracion_k.py`.

Por otro lado, se seleccionaron rangos  respaldados por la literatura, como una humedad inicial $M_0 = 50.0\%$ (base húmeda), dado que aproximadamente la mitad del peso del grano recién lavado corresponde a agua libre y ligada.También, se define una humedad de equilibrio $M_e = 10.0\%$, la cual actúa como límite termodinámico en el que la presión de vapor interna del café iguala a la del aire caliente y detiene la transferencia de masa. Finalmente, se delimita un ciclo de monitoreo de $24\text{ horas}$ con intervalos de $2\text{ horas}$

## 2. Fundamento Físico y Formulación Matemática

El movimiento del agua desde el interior del grano hacia su superficie está gobernado por la Segunda Ley de Fick. Debido a que la humedad cercana a la cáscara escapa más rápido que el agua atrapada en el núcleo, la solución exacta de este fenómeno de difusión corresponde a una serie infinita de decaimientos exponenciales (Serie de Fourier). Sin embargo, como los términos superiores se vuelven despreciables tras la primera hora de proceso, de esta simplificación surge inicialmente la **Ley de Secado de Thin-Layer**, la cual plantea que la velocidad de pérdida de humedad es proporcional a la fuerza impulsora $(M - M_e)$:

$$
\frac{dM}{dt} = -k(M - M_e)
$$

Al integrar esta ecuación diferencial desde $t = 0$ hasta cualquier instante $t$ y normalizar los datos mediante la humedad adimensional $Y$ (que escala todo el proceso entre $1$ y $0$), se obtiene una curva exponencial que asume un grano homogéneo sin resistencia geométrica inicial ($a = 1$):

$$
Y = \frac{M - M_e}{M_0 - M_e} = e^{-kt}
$$

No obstante, dado que el grano de café posee una geometría elipsoidal con hendidura central, se incorpora también el **Modelo de Henderson-Pabis**:

$$
Y = a \cdot e^{-kt}
$$

En esta expresión, el parámetro $a$ conserva las constantes geométricas del primer término de Fourier, actuando como un factor adimensional de forma que corrige las desviaciones estructurales respecto a una esfera perfecta.

## 3. Método Numérico: Regresión por Mínimos Cuadrados Ordinarios

Ajustar directamente funciones exponenciales exige algoritmos iterativos no lineales complejos; por ello, se aplica logaritmo natural ($\ln$) a ambos lados de las ecuaciones para transformarlas en relaciones lineales exactas. De este modo, el modelo de Thin-Layer adopta la forma de una recta forzada al origen ($y = -k \cdot x$), mientras que el modelo de Henderson-Pabis se convierte en una recta completa con intercepto ($y = b - k \cdot x$), donde $x = t$, $y = \ln(Y)$ y $b = \ln(a)$.

Al trasladar este planteamiento a los datos experimentales de `datos_secado_campo.csv`, surge el problema central de Métodos Numéricos: debido al error experimental propio de las mediciones, los $n = 12$ puntos registrados no se alinean de forma exacta. Esto configura un sistema sobredeterminado de doce ecuaciones para hallar dos incógnitas.

Para resolverlo, se implementa el método numérico de **Regresión por Mínimos Cuadrados Ordinarios (MCO)**, cuyo objetivo es encontrar los parámetros que minimizan la suma de los errores cuadráticos ($S$) entre los datos reales ($y_i$) y los valores estimados ($\hat{y}_i$). Para el modelo de Thin-Layer, se deriva la función de costo respecto a $k$ y se iguala a cero ($\frac{dS}{dk} = 0$), obteniendo la ecuación normal directa:

$$
S(k) = \sum_{i=1}^{n} (y_i + k \cdot x_i)^2 \quad \Longrightarrow \quad k = -\frac{\sum_{i=1}^{n} x_i y_i}{\sum_{i=1}^{n} x_i^2}
$$

Por su parte, al calibrar el modelo de Henderson-Pabis se minimiza una función de dos variables $S(b, m)$ igualando ambas derivadas parciales a cero ($\frac{\partial S}{\partial b} = 0$ y $\frac{\partial S}{\partial m} = 0$), lo que genera el Sistema de Ecuaciones Normales de Gauss ($2 \times 2$):

$$
\begin{cases}
n \cdot b + m \sum_{i=1}^{n} x_i = \sum_{i=1}^{n} y_i \\
b \sum_{i=1}^{n} x_i + m \sum_{i=1}^{n} x_i^2 = \sum_{i=1}^{n} x_i y_i
\end{cases}
$$

Una vez resuelto este sistema lineal, se recuperan los parámetros físicos originales mediante las transformaciones inversas $k = -m$ y $a = e^b$.

## 4. Validación Estadística y Ejecución del Código

Dado que el método de mínimos cuadrados siempre genera una recta óptima sin importar la naturaleza de los datos, resulta imprescindible evaluar el ajuste mediante el **Coeficiente de Determinación ($R^2$)**:

$$
R^2 = 1 - \frac{SS_{\text{res}}}{SS_{\text{tot}}} = 1 - \frac{\sum_{i=1}^{n} (y_i - \hat{y}_i)^2}{\sum_{i=1}^{n} (y_i - \bar{y})^2}
$$

Esta métrica compara el error residual del modelo ($SS_{\text{res}}$) frente a la variabilidad total respecto al promedio ($SS_{\text{tot}}$). Al alcanzar valores de $R^2 > 0.99$, se confirma que la física de capa delgada explica con más del $99\%$ de precisión el comportamiento experimental del café y valida numéricamente la constante $k$ calibrada.

# Leydy Andrea Salinas Diaz - Ingeniero de Software, Visualización y Git Master
# Diseñador del Pipeline, Gráficas y Documentación GitHub

Integrar los scripts de los compañeros, generar las visualizaciones científicas y mantener el repositorio profesional.

**Responsabilidades en el código y GitHub:**
1.** Unir los módulos de los Integrantes 1, 2 y 3 en un flujo de ejecución continuo y fácil de correr.
2.** Generar y exportar gráficas de alta calidad:
   - Curva de secado $M(t)$ vs. Tiempo con zona de humedad óptima sombreada (11%-12%).
   - Comparativa de error: RK4 vs. Euler.
   - Ajuste de Mínimos Cuadrados sobre los puntos experimentales.
3.** Crear el archivo `README.md` estructurado con la explicación matemática, el diagramado de variables y las instrucciones de instalación (`requirements.txt`).


# Camila - Interpolación y análisis de mermas

Desarrollé el módulo `src/interpolacion_mermas.py` para estimar valores de humedad en momentos en los que no se realizaron mediciones de campo y analizar la pérdida de masa de agua durante el proceso de secado del café.

**Interpolación de la humedad:**

Se implementaron dos métodos numéricos para estimar la humedad en tiempos intermedios: **Interpolación de Lagrange** y **Splines Cúbicos**. Estos métodos permiten obtener una aproximación de la humedad entre las mediciones experimentales disponibles.

La interpolación de Lagrange se basa en la construcción de un polinomio a partir de los puntos conocidos:

`P(x)=∑ yi Li(x)`

mientras que el método de Splines Cúbicos construye funciones polinómicas por tramos, proporcionando una curva suave entre las mediciones.

Como ejemplo, para una hora en la que no se realizó una medición directa, el programa estima la humedad mediante ambos métodos y permite comparar sus resultados.

**Integración numérica:**

Se programó la **Regla de Simpson 1/3** para calcular numéricamente la cantidad de agua evaporada durante el proceso de secado. Debido a que este método requiere puntos igualmente espaciados, se genera una serie temporal uniforme para realizar la integración de la tasa de evaporación.

La integración se expresa como una aproximación del área bajo la curva de la tasa de evaporación:

`Agua evaporada ≈ ∫ tasa de evaporación dt`

**Cálculo de la tasa de evaporación:**

A partir de las mediciones de humedad y una masa inicial del lote, se estima la cantidad de agua presente en el grano suponiendo que la materia seca permanece constante. A partir de la variación de esta cantidad de agua con respecto al tiempo se obtiene la tasa de evaporación en kg/h.

**Balance de masa:**

Finalmente, se calcula la masa final del lote y la merma porcentual producida por la pérdida de agua:

`Masa final = Masa inicial − Agua evaporada`

`Merma (%) = (Agua evaporada / Masa inicial) × 100`

El módulo también permite cargar directamente los datos experimentales desde `data/datos_secado_campo.csv` y ejecutar todo el procedimiento desde un único programa.

## Integrante 2: Programador del Algoritmo Numérico (EDOs)
**Estudiante:** Juan Carlos León Ramos

### Responsabilidades desarrolladas:
1. **Algoritmo RK4:** Implementación desde cero del método de Runge-Kutta de 4º Orden en `src/metodos_edo.py`.
2. **Algoritmo de Euler:** Implementación comparativa de precisión y error según el tamaño de paso $h$.
3. **Cálculo de parada:** Identificación del tiempo óptimo de secado (rango del 11% al 12% de humedad para Café Pergamino Seco).
4. **Pruebas unitarias:** Módulo de validación de modelos en `tests/test_rk4.py`.

## Juan Carlos León Ramos - Integrante 2: Programador del Algoritmo Numérico (EDOs)

Implementación de los métodos numéricos para resolver la ecuación diferencial del proceso de secado de café[cite: 1]:

$$\frac{dM}{dt} = -k(M - M_e)$$

### Métodos e Implementación:

1. **Algoritmo Runge-Kutta de 4º Orden (RK4):**
   Programación desde cero del algoritmo RK4 para integrar numéricamente la EDO del secado[cite: 1]:
   $$k_1 = f(t_i, M_i)$$
   $$k_2 = f\left(t_i + \frac{h}{2}, M_i + \frac{h}{2}k_1\right)$$
   $$k_3 = f\left(t_i + \frac{h}{2}, M_i + \frac{h}{2}k_2\right)$$
   $$k_4 = f(t_i + h, M_i + h k_3)$$
   $$M_{i+1} = M_i + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$

2. **Algoritmo de Euler (Comparativo):**
   Implementación del método de Euler para realizar un análisis comparativo de precisión y error frente a RK4 según el paso $h$[cite: 1]:
   $$M_{i+1} = M_i + h \cdot f(t_i, M_i)$$

3. **Cálculo de Parada:**
   Identifica la hora exacta en la que el café alcanza la humedad objetivo del **11% al 12%** (Café Pergamino Seco)[cite: 1].
