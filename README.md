# ProyectoFinalMetodos
# Mermas de secado del café 
# Laura Sofia Bolivar Jimenez - Modelamiento fisico y calibracion de datos
Formula la física del proceso de secado de café mediante la Ley de Secado de Thin-Layer y programar en Python la estimación del parámetro óptimo k (constante de secado) utilizando el método de Mínimos Cuadrados, evaluando el ajuste con el coeficiente de determinación R^2.
**Modelo de Thin-Layer (Ecuación Diferencial)** 
La tasa de cambio de humedad en el grano es proporcional a la diferencia entre su humedad actual M y la humedad de equilibrio M_e:
   $$\frac{dM}{dt} = -k(M - M_e)$$

**Linealización de Datos (Transformación $y = m \cdot x$):**  
Definiendo la humedad adimensional $Y = \frac{M - M_e}{M_0 - M_e}$, la ecuación se linealiza aplicando logaritmo natural:
   $$y = \ln(Y) \quad \text{donde} \quad y = -k \cdot x \quad (x = t)$$

**Calibración mediante Mínimos Cuadrados:**  
Minimizando la suma de errores al cuadrado $S(k) = \sum (y_i + k \cdot x_i)^2$, la pendiente $-k$ óptima se calcula derivando e igualando a cero:
   $$k = -\frac{\sum x_i y_i}{\sum x_i^2}$$

**Calidad del Ajuste ($R^2$):**  
Se mide la precisión del modelo ajustado frente a los datos experimentales mediante:
   $$R^2 = 1 - \frac{SS_{res}}{SS_{tot}} = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$$

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
