import random
from collections import deque

# -----------------------------
# CONFIGURACIÓN INICIAL
# -----------------------------
TMax = 1200                     # Tiempo máximo de simulación (minutos)
TM = 0                          # Tiempo actual del modelo
n = 1500                         # Número máximo de pasajeros

# Generación pseudoaleatoria de tiempos
TI = [random.randint(1, 8) for _ in range(n)]        # Tiempos entre llegadas
TA = [random.randint(5, 15) for _ in range(n)]       # Tiempos de atención

# Variables del sistema
pasajero = 1
ocupado = False                 # Estado del aforador
llegada = TI[0]                 # Tiempo de llegada del primer pasajero
salida = float('inf')           # Tiempo de salida inicial (ninguno)
ta = 0                          # Contador de tiempos de atención

# Estructuras de datos
eventos = []                    # Lista de eventos
fila = deque()                  # Cola de espera

# -----------------------------
# SIMULACIÓN CON FILA
# -----------------------------
print("\n--- SIMULACIÓN CON FILA ---")

while TM <= TMax:
    # Llega un pasajero
    if llegada < salida:
        TM = llegada

        if not ocupado:
            # Aforador desocupado → atender directamente
            ocupado = True
            salida = TM + TA[ta]
            ta += 1
            evento = ("Entrada y Atención", pasajero, TM, salida, "Atendido")
        else:
            # Aforador ocupado → pasajero entra a la fila
            fila.append(pasajero)
            evento = ("Entrada", pasajero, TM, TM, "No Atendido")

        eventos.append(evento)
        pasajero += 1

        # Programar próxima llegada
        if pasajero < n:
            llegada = TM + TI[pasajero - 1]
        else:
            break
    # Sale un pasajero
    else:
        TM = salida
        evento = ("Salida", "-", TM, salida, "Atendido")
        eventos.append(evento)

        if fila:
            # Hay pasajeros esperando → atender siguiente
            siguiente = fila.popleft()
            salida = TM + TA[ta]
            ta += 1
            evento = ("Atención desde fila", siguiente, TM, salida, "Atendido")
            eventos.append(evento)
        else:
            # Sin fila → aforador libre
            ocupado = False
            salida = float('inf')

# -----------------------------
# RESUMEN DE RESULTADOS
# -----------------------------
atendidos = [e for e in eventos if e[4] == "Atendido" and isinstance(e[1], int)]
no_atendidos = [e for e in eventos if e[4] == "No Atendido"]

print(f"\nTotal de eventos registrados: {len(eventos)}")
print(f"Total de pasajeros procesados: {pasajero - 1}")
print(f"Pasajeros atendidos: {len(atendidos)}")
print(f"Pasajeros no atendidos: {len(no_atendidos)}")

# -----------------------------
# Tiempo promedio de atención
# -----------------------------
duraciones = [e[3] - e[2] for e in atendidos if isinstance(e[3], (int, float))]
if duraciones:
    promedio_tiempo = sum(duraciones) / len(duraciones)
    print(f"\nSolución → Tiempo promedio de atención: {promedio_tiempo:.2f} minutos")
else:
    promedio_tiempo = 0
    print("\nSolución → No hubo tiempos de atención válidos.")

# -----------------------------
# PREGUNTAS Y RESULTADOS
# -----------------------------
print("\n--- SECCIÓN DE PREGUNTAS ---")

# 1) ¿Cuántos pasajeros no fueron atendidos?
print("\n1) ¿Cuántos pasajeros no fueron atendidos?")
print(f"   → {len(no_atendidos)} pasajeros")

# 2) ¿Cuántos pasajeros entraron y salieron en un minuto impar?
impares_total = [
    e for e in eventos
    if isinstance(e[2], (int, float)) and isinstance(e[3], (int, float))
    and int(e[2]) % 2 != 0 and int(e[3]) % 2 != 0
]
print("\n2) ¿Cuántos pasajeros entraron y salieron en un minuto impar?")
print(f"   → {len(impares_total)} pasajeros")

# 3) ¿Cuántos pasajeros atendidos entraron y salieron en un minuto impar?
impares_atendidos = [
    e for e in atendidos
    if int(e[2]) % 2 != 0 and int(e[3]) % 2 != 0
]
print("\n3) ¿Cuántos pasajeros atendidos entraron y salieron en un minuto impar?")
print(f"   → {len(impares_atendidos)} pasajeros")

# -----------------------------
# PREGUNTAS PROPUESTAS ADICIONALES
# -----------------------------
print("\n--- PREGUNTAS PROPUESTAS ---")

# 4) ¿Cuál fue el mayor tiempo de inactividad del aforador?
max_inactividad = 0
for i in range(1, len(eventos)):
    if eventos[i-1][0] == "Salida" and eventos[i][0].startswith("Entrada"):
        tiempo = eventos[i][2] - eventos[i-1][2]
        if tiempo > max_inactividad:
            max_inactividad = tiempo
print("\n4) ¿Cuál fue el mayor tiempo de inactividad del aforador?")
print(f"   → {max_inactividad} minutos")

# 5) ¿Cuál fue el número máximo de personas en fila simultáneamente?
max_fila = 0
fila_actual = 0
for e in eventos:
    if e[4] == "No Atendido":
        fila_actual += 1
    elif e[0] in ("Atención desde fila", "Salida"):
        fila_actual = max(fila_actual - 1, 0)
    max_fila = max(max_fila, fila_actual)
print("\n5) ¿Cuál fue el número máximo de personas en fila simultáneamente?")
print(f"   → {max_fila} personas")

# 6) ¿Cuántos pasajeros atendidos estuvieron menos de 6 minutos en total en el sistema?
rapidos = [e for e in atendidos if (e[3] - e[2]) < 6]
print("\n6) ¿Cuántos pasajeros atendidos estuvieron menos de 6 minutos en el sistema?")
print(f"   → {len(rapidos)} pasajeros")
