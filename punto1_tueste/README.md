***# Proyecto: Medición de Curvaturas y RoR en el Tueste del Café***



***## Descripción del Proyecto***

***Este proyecto aplica \*\*Métodos Numéricos\*\* mediante Python (JupyterLab y Miniconda) para analizar la evolución térmica del grano de café durante el proceso de tueste. A partir de una curva sigmoide de temperatura respecto al tiempo $T(t)$, se calcula la tasa de ascenso (\*Rate of Rise\* - RoR) y la curvatura geométrica $K(t)$ para identificar puntos críticos de inflexión, tales como las reacciones endotérmicas, exotérmicas y el \*First Crack\*.***



***## Fundamento Matemático***

***1. \*\*Diferenciación Numérica (Diferencias Finitas):\*\****

&#x20;  ***- \*\*Hacia adelante:\*\* Aplicada en el extremo inicial ($t\_0$).***

&#x20;  ***- \*\*Centradas:\*\* Aplicada en los nodos interiores ($t\_1, \\dots, t\_{n-1}$) para mayor precisión.***

&#x20;  ***- \*\*Hacia atrás:\*\* Aplicada en el extremo final ($t\_n$).***

***2. \*\*Primera Derivada ($T'(t) = dT/dt$):\*\* Representa el \*Rate of Rise\* (RoR), indicador clave del perfil de sabor.***

***3. \*\*Segunda Derivada ($T''(t)$) y Curvatura Geométrica ($K$):\*\****

&#x20;  ***$$K(t) = \\frac{|T''(t)|}{(1 + \[T'(t)]^2)^{3/2}}$$***



***## Estructura del Repositorio***

***\* `datos/`: Datasets en formato `.csv` / `.xlsx` con los registros de tiempo ($t$) y temperatura del grano ($T$).***

***\* `integrantes/`: Carpetas individuales con los notebooks de desarrollo (`.ipynb`) de cada miembro del equipo.***

***\* `resultados\_finales/`: Gráficas de $T(t)$, $RoR(t)$, $K(t)$ y tablas numéricas consolidadas.***

***\* `informe/`: Documentación técnica, análisis de resultados y conclusiones del tueste.***

***\* `referencias/`: Bibliografía sobre cinética de tueste y diferenciación numérica.***



***## Integrantes y Roles***

***\* \*\*Integrante 1 (Datos y Curva Base):\*\* Recolección/simulación de datos térmicos y limpieza en `datos/`.***

***\* \*\*Integrante 2 (Diferencias Finitas):\*\* Programación de esquemas hacia adelante, centrados y hacia atrás para hallar $T'(t)$ y $T''(t)$.***

***\* \*\*Integrante 3 (Curvatura $K$ e Informe):\*\* Cálculo de $K(t)$, identificación del \*First Crack\*, gráficas finales e informe.***



***## Entorno y Ejecución***

***1. Abrir \*\*Anaconda Prompt (Miniconda)\*\* y activar el entorno de trabajo:***

&#x20;  ***```bash***

&#x20;  ***conda activate nombre\_tu\_entorno***

&#x20;  ***jupyter lab***

