import random
import json

class CromosomaGrafo:
    def __init__(self):
        # 1. EL IDIOMA GENÉTICO: Matriz 6x6 inicializada en ceros
        self.matriz = [[0 for _ in range(6)] for _ in range(6)]

    def generar_grafo_aleatorio(self):
        # Llenamos la matriz con algunos caminos al azar para empezar
        self.matriz = [[0 for _ in range(6)] for _ in range(6)]

        for i in range(6):
            for j in range(6):
                if j != i:
                    # 30% de probabilidad de crear una arista con costo 1-9
                    if random.random() < 0.3:
                        self.matriz[i][j] = random.randint(1, 9)

    def obtener_formato_profesor(self):
        # 2. EL ADAPTADOR: Leemos la matriz y armamos la lista
        aristas_formato_final = []

        for origen in range(6):
            for destino in range(6):
                costo = self.matriz[origen][destino]

                # Si el costo es mayor a 0, guardamos la arista
                if costo > 0:
                    aristas_formato_final.append([origen, destino, costo])

        # 3. EL IDIOMA DEL PROFESOR: Devolvemos el diccionario exacto que pide
        return {
            "n": 6,
            "inicio": 0,
            "meta": 5,
            "aristas": aristas_formato_final
        }


def ejecutar_linea_base_aleatoria(semilla, presupuesto=1000):
    # 1. Controlar la fuente de aleatoriedad (Requerimiento 8)
    random.seed(semilla)

    # Variables para el registro experimental (Requerimiento 9)
    primer_hallazgo = None
    grafos_evaluados = 0

    print(f"--- Iniciando Búsqueda Aleatoria (Semilla: {semilla}) ---")

    for evaluacion_actual in range(1, presupuesto + 1):
        # 2. Generar candidato desde cero usando la misma distribución (Requerimiento 6)
        candidato = CromosomaGrafo()
        candidato.generar_grafo_aleatorio()
        grafos_evaluados += 1

        # 3. Adaptar al formato JSON del profesor
        grafo_json = candidato.obtener_formato_profesor()

        # 4. Evaluar con el paquete docente (Presupuesto de 100 expansiones por defecto)
        # informe = evaluar(grafo_json, limite_expansiones=100)

        # --- SIMULACIÓN DEL INFORME PARA ESTE EJEMPLO ---
        # En tu código real, esto lo devuelve la función evaluar() del profesor
        informe = {
            "B1": {"verificacion": {"contraejemplo": False, "discrepancias": []}},
            "U1": {"verificacion": {"contraejemplo": False, "discrepancias": []}},
            "A1": {"verificacion": {"contraejemplo": False, "discrepancias": []}}
        }
        # ------------------------------------------------

        # 5. Revisar si los agentes devolvieron un contraejemplo confirmado
        for agente, resultado in informe.items():
            verificacion = resultado.get("verificacion", {})

            # Si el profesor confirma que encontramos un defecto
            if verificacion.get("contraejemplo") is True:
                discrepancia = verificacion.get("discrepancias", [])

                # Registramos en qué evaluación apareció el primer error
                if primer_hallazgo is None:
                    primer_hallazgo = {
                        "agente_fallido": agente,
                        "evaluacion_numero": evaluacion_actual,
                        "tipo_error": discrepancia,
                        "grafo": grafo_json
                    }
                    print(f"¡DEFECTO ENCONTRADO EN {agente}! (Evaluación {evaluacion_actual})")
                    print(f"Error: {discrepancia}")

                    # No usamos 'break' aquí porque el requerimiento 7 exige consumir
                    # el presupuesto completo o al menos seguir buscando otros errores.

        # (Opcional) Aquí deberías calcular y guardar la "aptitud" de este grafo
        # para tus gráficas de progreso, aunque en este método no uses esa aptitud para seleccionar.

    # 6. Reporte final tras agotar el presupuesto de 1000
    if primer_hallazgo:
        print("Búsqueda finalizada: Se encontró al menos un contraejemplo.")
    else:
        print("Búsqueda finalizada: no encontrado.") # Requerimiento 9: honestidad sin inventar

    return primer_hallazgo


# Ejecutar el experimento con la primera semilla exigida
# resultado_semilla_11 = ejecutar_linea_base_aleatoria(semilla=11, presupuesto=1000)

# --- PRUEBA DEL CÓDIGO ---
# Creamos tu individuo
mi_individuo = CromosomaGrafo()
mi_individuo.generar_grafo_aleatorio()

# Lo traducimos
grafo_para_evaluar = mi_individuo.obtener_formato_profesor()

# Así se ve lo que le vas a mandar al código de tu profesor:
print(json.dumps(grafo_para_evaluar, indent=2))