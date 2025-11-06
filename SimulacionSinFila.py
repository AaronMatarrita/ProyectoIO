import random

# -----------------------------
# CONFIGURACIÓN INICIAL
# -----------------------------
TMax = 1000                      # Tiempo máximo de simulación
TM = 0                           # Tiempo actual del modelo
llegada = random.randint(1, 10)  # Tiempo de la primera llegada
salida = float('inf')
pasajero = 1
desocupado = True
pasajeroSiendoAtendido = 0

eventos = [["Evento", "#Pasajero", "TM", "Revisión"]]

# -----------------------------
# SIMULACIÓN SIN FILA
# -----------------------------
print("\n--- SIMULACIÓN SIN FILA ---")

while TM <= TMax:
    if llegada < salida:
        # Procesar llegada
        TM = llegada

        if desocupado:
            # Inicia revisión
            desocupado = False
            TA = random.randint(1, 10)
            salida = TM + TA
            pasajeroSiendoAtendido = pasajero
            eventos.append(["Entrada", pasajeroSiendoAtendido, TM, "Rev"])
        else:
            # Pasa sin revisión
            eventos.append(["Entró y salió", pasajero, TM, "No Rev"])

        # Planificar próxima llegada
        TI = random.randint(1, 10)
        llegada = TM + TI
        pasajero += 1

    else:
        # Procesar salida
        TM = salida
        eventos.append(["Salida", pasajeroSiendoAtendido, TM, "Rev"])
        desocupado = True
        salida = float('inf')

# -----------------------------
# RESUMEN DE LA SIMULACIÓN
# -----------------------------
revisados = [e for e in eventos if e[0] == "Entrada" and e[3] == "Rev"]
no_revisados = [e for e in eventos if e[3] == "No Rev"]

print(f"\nTotal de eventos registrados: {len(eventos)-1}")
print(f"Total de pasajeros procesados: {pasajero - 1}")
print(f"Pasajeros atendidos (revisados): {len(revisados)}")
print(f"Pasajeros sin revisar: {len(no_revisados)}")

# -----------------------------
# REGISTRO DE EVENTOS
# -----------------------------
print("\n--- REGISTRO DE EVENTOS ---")
for e in eventos:
    print(f"{e[0]:<15} {str(e[1]):<10} {str(e[2]):<6} {e[3]:<10}")

# -----------------------------
# PREGUNTAS Y RESULTADOS
# -----------------------------
print("\n--- SECCIÓN DE PREGUNTAS ---")

# 1. Pasajeros que se fueron atendidos
print("\n1) ¿Cuáles pasajeros se fueron atendidos?")
print(f"   → Total atendidos: {len(revisados)}")
print(f"   → Pasajeros atendidos: {[e[1] for e in revisados]}")

# 2. Tiempo total que el aforador estuvo desocupado
tiempo_desocupado = 0
for i in range(1, len(eventos)):
    if eventos[i-1][0] == "Salida" and eventos[i][0] == "Entrada":
        tiempo_desocupado += eventos[i][2] - eventos[i-1][2]

print("\n2) ¿Cuánto tiempo estuvo el aforador desocupado?")
print(f"   → {tiempo_desocupado} minutos")

# 3. Pasajeros que llegaron en minuto impar
llegadas_impares = [e[1] for e in eventos if e[0] == "Entrada" and e[2] % 2 != 0]
print("\n3) ¿Cuáles pasajeros llegaron en un minuto impar?")
print("   →", llegadas_impares if llegadas_impares else "Ninguno")

# -----------------------------
# PREGUNTAS PROPUESTAS ADICIONALES
# -----------------------------
print("\n--- PREGUNTAS PROPUESTAS ---")

print("\n4) ¿Cuál fue el tiempo promedio de atención?")
tiempos_atencion = []
for i in range(1, len(eventos)):
    if eventos[i-1][0] == "Entrada" and eventos[i][0] == "Salida" and eventos[i-1][1] == eventos[i][1]:
        tiempos_atencion.append(eventos[i][2] - eventos[i-1][2])
if tiempos_atencion:
    print(f"   → Promedio: {sum(tiempos_atencion)/len(tiempos_atencion):.2f} min")
else:
    print("   → No hubo registros de atención.")

print("\n5) ¿Cuáles pasajeros se fueron sin revisar?")
sin_revisar = [e[1] for e in eventos if e[3] == "No Rev"]
print("   →", sin_revisar if sin_revisar else "Ninguno")

print("\n6) ¿Cuál fue el mayor tiempo de inactividad del aforador?")
max_inactividad = 0
for i in range(1, len(eventos)):
    if eventos[i-1][0] == "Salida" and eventos[i][0] == "Entrada":
        inact = eventos[i][2] - eventos[i-1][2]
        if inact > max_inactividad:
            max_inactividad = inact
print(f"   → Mayor periodo desocupado: {max_inactividad} minutos")