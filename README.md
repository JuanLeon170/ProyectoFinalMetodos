# ProyectoFinalMetodos
# Mermas de secado del café 
# Laura Sofia Bolivar Jimenez - Modelamiento fisico y calibracion de datos
Formula la física del proceso de secado de café mediante la Ley de Secado de Thin-Layer y programar en Python la estimación del parámetro óptimo k (constante de secado) utilizando el método de Mínimos Cuadrados, evaluando el ajuste con el coeficiente de determinación R^2.

# Modelo de Thin-Layer (Ecuación Diferencial)  
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
