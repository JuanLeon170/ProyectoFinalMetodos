md = """
### TABLA 1: VARIACION DE DOSIS

| Fila | Dosis (g) | Rendimiento (g) | Ratio (g/g) | Tiempo est. (s) | Caudal (g/s) | EY sim (%) | Diagnostico |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| 0 | 15.0 | 45.0 | 3.00 | 25.8 | 1.74 | 18.80 | Zona equilibrada |
| 1 | 16.5 | 45.0 | 2.73 | 26.9 | 1.67 | 18.37 | Zona equilibrada |
| 2 | 18.0 | 45.0 | 2.50 | 28.0 | 1.61 | 18.00 | Zona equilibrada |
| 3 | 19.5 | 45.0 | 2.31 | 29.0 | 1.55 | 17.66 | Zona equilibrada |
| 4 | 21.0 | 45.0 | 2.14 | 30.0 | 1.50 | 17.35 | Zona equilibrada |

### TABLA 2: VARIACION DE RENDIMIENTO / RATIO

| Fila | Dosis (g) | Rendimiento (g) | Ratio (g/g) | Tiempo est. (s) | Caudal (g/s) | EY sim (%) | Diagnostico |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| 0 | 18.0 | 30.0 | 1.67 | 18.7 | 1.60 | 14.12 | Subextraccion / flujo rapido |
| 1 | 18.0 | 36.0 | 2.00 | 22.4 | 1.61 | 15.74 | Subextraccion / flujo rapido |
| 2 | 18.0 | 45.0 | 2.50 | 28.0 | 1.61 | 18.00 | Zona equilibrada |
| 3 | 18.0 | 54.0 | 3.00 | 33.6 | 1.61 | 20.08 | Zona equilibrada |
| 4 | 18.0 | 63.0 | 3.50 | 39.2 | 1.61 | 22.03 | Sobreextraccion / flujo lento |

### TABLA 3: VARIACION DE TEMPERATURA

| Fila | Temp. agua (C) | Tiempo est. (s) | Caudal (g/s) | EY sim (%) | Diagnostico |
| :--- | :---: | :---: | :---: | :---: | :--- |
| 0 | 90.0 | 28.5 | 1.58 | 17.39 | Zona equilibrada |
| 1 | 93.0 | 28.3 | 1.59 | 17.71 | Zona equilibrada |
| 2 | 96.0 | 28.0 | 1.61 | 18.00 | Zona equilibrada |
| 3 | 98.0 | 27.8 | 1.62 | 18.19 | Zona equilibrada |
| 4 | 99.0 | 27.7 | 1.62 | 18.29 | Zona equilibrada |

### TABLA 4: VARIACION DE PRESION

| Fila | Presion (bar) | Rango ref. (19-20) | Tiempo est. (s) | Caudal (g/s) | EY sim (%) | Diagnostico |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| 0 | 16.0 | Fuera | 26.5 | 1.70 | 17.75 | Zona equilibrada |
| 1 | 18.0 | Fuera | 27.4 | 1.64 | 17.90 | Zona equilibrada |
| 2 | 19.5 | Dentro | 28.0 | 1.61 | 18.00 | Zona equilibrada |
| 3 | 20.0 | Dentro | 28.2 | 1.60 | 18.05 | Zona equilibrada |
"""

with open("README.md", "a", encoding="utf-8") as f:
    f.write(md)

print("OK: README.md actualizado")
