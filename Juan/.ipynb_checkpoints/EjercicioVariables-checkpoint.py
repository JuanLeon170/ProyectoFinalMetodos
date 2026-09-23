# ==========================================
# PROBLEMA AMBIENTAL: MONITOREO DE CAUDAL Y CALIDAD
# ==========================================
nombre_estacion = "Estación Río Botello"
ph_agua = 7.2
oxigeno_disuelto_mg_l = 6.5
cumple_normativa = True

print("=== REPORTE DE MONITOREO AMBIENTAL ===")
print("Punto de muestreo:", nombre_estacion)
print("pH del agua:", ph_agua)
print("Oxígeno Disuelto (mg/L):", oxigeno_disuelto_mg_l)
print("¿Cumple con la normativa para uso agrícola?:", cumple_normativa)
print("\n" + "="*40 + "\n")

# ==========================================
# EJERCICIOS PRÁCTICOS
# ==========================================

# EJERCICIO 1: ÁREA DE UN TRIÁNGULO
print("--- EJERCICIO 1: Cálculo de Área ---")
base_triangulo = float(input("Ingrese la base del triángulo (m): "))
altura_triangulo = float(input("Ingrese la altura del triángulo (m): "))
area_calculada = (base_triangulo * altura_triangulo) / 2
print(f"El área del triángulo calculada es: {area_calculada} m²\n")

# EJERCICIO 2: EL DOBLE Y EL RESIDUO DE UN NÚMERO
print("--- EJERCICIO 2: Operaciones con Enteros ---")
numero_ingresado = int(input("Ingrese un número entero para evaluar: "))
doble_valor = numero_ingresado * 2
residuo_dos = numero_ingresado % 2
print(f"El doble de {numero_ingresado} es: {doble_valor}")
print(f"El residuo de dividir {numero_ingresado} entre 2 es: {residuo_dos}\n")

# EJERCICIO 3: CUATRO TIPOS DE DATOS Y SUS FUNCIONES type()
print("--- EJERCICIO 3: Verificación de Tipos de Datos ---")
temperatura_promedio = 18.4          # float
cantidad_muestras = 12               # int
cuenca_hidrica = "Cuenca Alta"       # str
alerta_activa = False                # bool

print("temperatura_promedio:", temperatura_promedio, "-> Tipo:", type(temperatura_promedio))
print("cantidad_muestras:", cantidad_muestras, "-> Tipo:", type(cantidad_muestras))
print("cuenca_hidrica:", cuenca_hidrica, "-> Tipo:", type(cuenca_hidrica))
print("alerta_activa:", alerta_activa, "-> Tipo:", type(alerta_activa))