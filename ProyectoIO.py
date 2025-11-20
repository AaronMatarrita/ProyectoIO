# ============================================================
# ProyectoIO.py
# Simulación SIN fila y Simulación CON fila
# Estudiantes: Aaron Matarrita Portuguez, Edgar Amador Lazo, Gonzalo Dormos Rodríguez
# ------------------------------------------------------------
# Nota*: En el video se muestran dos archivos separados (SimulacionSinFila.py y SimulacionConFila.py).
# Aquí ambos se integran en un solo código, según lo solicitado en el aula virtual.
# ============================================================

import random
from collections import deque

# -----------------------------
# SIMULACIÓN SIN FILA
# -----------------------------

def simulacion_sin_fila():
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
    print("\n==============================")
    print("       SIMULACIÓN SIN FILA     ")
    print("==============================")

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
        if (
            eventos[i-1][0] == "Entrada"
            and eventos[i][0] == "Salida"
            and eventos[i-1][1] == eventos[i][1]
        ):
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


# -----------------------------
# SIMULACIÓN CON FILA
# -----------------------------

def simulacion_con_fila():
    # -----------------------------
    # CONFIGURACIÓN INICIAL
    # -----------------------------
    TMax = 1200                     # Tiempo máximo de simulación (minutos)
    TM = 0                          # Tiempo actual del modelo
    n = 500                         # Número máximo de pasajeros

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
    print("\n==============================")
    print("       SIMULACIÓN CON FILA     ")
    print("==============================")

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
    duraciones = [
        e[3] - e[2]
        for e in atendidos
        if isinstance(e[3], (int, float))
    ]
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
        if isinstance(e[2], (int, float))
        and isinstance(e[3], (int, float))
        and int(e[2]) % 2 != 0
        and int(e[3]) % 2 != 0
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


if __name__ == "__main__":
    simulacion_sin_fila()
    simulacion_con_fila()
