"""Representación de grafos y línea base aleatoria (código del equipo).

Depende del paquete docente ``busqueda`` versión 1.0.0, que no se modifica.
"""

import json
import random
import time
from pathlib import Path

from busqueda import evaluar, validar, ejecutar, heuristica, verificar

AGENTES = ("B1", "U1", "A1")


class CromosomaGrafo:
    def __init__(self):
        self.matriz = [[0 for _ in range(6)] for _ in range(6)]

    def generar_grafo_aleatorio(self, rng=None):
        if rng is None:
            rng = random

        self.matriz = [[0 for _ in range(6)] for _ in range(6)]
        for i in range(6):
            for j in range(6):
                if i != j and rng.random() < 0.3:
                    self.matriz[i][j] = rng.randint(1, 9)

    def obtener_formato_profesor(self):
        aristas = []
        for origen in range(6):
            for destino in range(6):
                costo = self.matriz[origen][destino]
                if costo > 0:
                    aristas.append([origen, destino, costo])

        return {"n": 6, "inicio": 0, "meta": 5, "aristas": aristas}

def comporbar_y_guardar_contraejemplo(grafo_json, agente, metodo, semilla, num_evaluacion, ruta_archivo):
    print(f"Comprobando posible contraejemplo para {agente}")

    try:
        resultadoAgente = ejecutar(agente, grafo_json, limite_expansiones=100)
    except Exception as e:
        print(f"Descartado: El grafo provoco un fallo({e})")
        return False

    diagnostico = verificar(agente, grafo_json,resultadoAgente)

    if diagnostico.get("contraejemplo") is True:
        discrepancias = diagnostico.get("discrepancias", [])

        evidencia = {
            "metodo": metodo,
            "semilla": semilla,
            "numero_evaluacion": num_evaluacion,
            "agente": agente,
            "grafo": grafo_json,
            "resultado_referencia":diagnostico.get("referencia"),
            "incumplimiento":discrepancias,
            "explicacion": f"El agente {agente} fallo la validacion. Discrepancia detectada:{', '.join(discrepancias)}"
        }

        if agente == 'A1':
            evidencia['heristica_utilizada'] = heuristica(grafo_json)


        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(evidencia, f , indent=2, ensure_ascii=False)

        print(f'Exito!!! Contraejemplo confirmado y guardado en {ruta_archivo}')
        return True

    else:
        print('Falsa alarma: EL resultado fue limite, error, o el agente actuo correctamente.')
        return False
    

def ejecutar_linea_base_aleatoria(semilla=11, presupuesto=1000, limite_expansiones=100):
    """Evalúa grafos independientes; no es el algoritmo genético."""
    rng = random.Random(semilla)
    carpeta = Path("resultados")
    carpeta.mkdir(exist_ok=True)

    prefijo = f"aleatoria_semilla_{semilla}"
    ruta_detalle = carpeta / f"{prefijo}_evaluaciones.jsonl"
    ruta_resumen = carpeta / f"{prefijo}_resumen.json"

    primeros_hallazgos = {agente: None for agente in AGENTES}
    hallazgos_acumulados = {agente: 0 for agente in AGENTES}
    incidencias = {agente: {"limite": 0, "error": 0} for agente in AGENTES}
    claves_distintas = set()
    progreso = []
    inicio = time.perf_counter()

    print(f"Iniciando línea base aleatoria | semilla={semilla} | presupuesto={presupuesto}")

    with ruta_detalle.open("w", encoding="utf-8") as archivo:
        for numero in range(1, presupuesto + 1):
            candidato = CromosomaGrafo()
            candidato.generar_grafo_aleatorio(rng)
            grafo = candidato.obtener_formato_profesor()

            try:
                validar(grafo)
            except ValueError as exc:
                raise RuntimeError(
                    f"Candidato inválido en el intento {numero}; revisar el código propio: {exc}"
                ) from exc

            clave = json.dumps(grafo, sort_keys=True, separators=(",", ":"))
            claves_distintas.add(clave)

            try:
                informe = evaluar(grafo, limite_expansiones=limite_expansiones)
            except Exception as exc:
                raise RuntimeError(
                    f"Fallo de integración/evaluación en el candidato {numero}: {exc}"
                ) from exc

            archivo.write(json.dumps({
                "evaluacion": numero,
                "grafo": grafo,
                "informe": informe,
            }, ensure_ascii=False) + "\n")

            for agente in AGENTES:
                resultado = informe[agente]["resultado"]
                verificacion = informe[agente]["verificacion"]
                estado = resultado["estado"]

                if estado in ("limite", "error"):
                    incidencias[agente][estado] += 1
                elif verificacion["concluyente"] and verificacion["contraejemplo"]:
                    hallazgos_acumulados[agente] += 1
                    if primeros_hallazgos[agente] is None:
                        primeros_hallazgos[agente] = {
                            "evaluacion": numero,
                            "grafo": grafo,
                            "resultado": resultado,
                            "verificacion": verificacion,
                        }

            if numero % 100 == 0 or numero == presupuesto:
                progreso.append({
                    "evaluaciones": numero,
                    "grafos_distintos": len(claves_distintas),
                    "hallazgos_acumulados": hallazgos_acumulados.copy(),
                    "incidencias": {a: incidencias[a].copy() for a in AGENTES},
                })
                archivo.flush()
                print(f"{numero}/{presupuesto} evaluaciones | "
                      f"hallazgos B1={hallazgos_acumulados['B1']}, "
                      f"U1={hallazgos_acumulados['U1']}, "
                      f"A1={hallazgos_acumulados['A1']}")

    resumen = {
        "metodo": "aleatoria",
        "semilla": semilla,
        "presupuesto": presupuesto,
        "limite_expansiones": limite_expansiones,
        "probabilidad_arista": 0.3,
        "rango_costos": [1, 9],
        "evaluaciones_consumidas": presupuesto,
        "grafos_distintos": len(claves_distintas),
        "hallazgos_confirmados": hallazgos_acumulados,
        "primer_hallazgo_por_agente": primeros_hallazgos,
        "incidencias": incidencias,
        "progreso": progreso,
        "tiempo_segundos": round(time.perf_counter() - inicio, 3),
    }
    ruta_resumen.write_text(json.dumps(resumen, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nRegistros guardados: {ruta_detalle} y {ruta_resumen}")
    for agente in AGENTES:
        hallazgo = primeros_hallazgos[agente]
        print(f"{agente}: evaluación {hallazgo['evaluacion']}" if hallazgo else
              f"{agente}: no encontrado")
    return resumen


def evaluar_individuo(candidato, limite_expansiones=100):
    """
    Evalúa un cromosoma y devuelve información
    para el algoritmo genético.
    1 Recibe un cromosoma de la clase de cromosoma grafo
    2- convierte el grafo al formato del profe
    3 valida
    4 evalua los distintos algoritmos
    5 recopila resultados
    6 devuelver informacion

    puedes llamar la funcion con "from grafos import CromosomaGrafo, evaluar_individuo"
    """

    # Aqui transformamos la matriz de 6x6 al formato del profe
    grafo = candidato.obtener_formato_profesor()

    #aqui validamos los gragos
    validar(grafo)

    # Aqui ejecutamos los algoritmos del profe
    informe = evaluar(
        grafo,
        limite_expansiones=limite_expansiones
    )

    # Aqui entra un concepto de la aptitud Carlos, muy poosiblemente tengas que cambiar esta parte pues no la entiendo que 
    # y que vas a necesitar
    resultados = {}

    for agente in AGENTES:
        datos = informe[agente]

        resultado = datos["resultado"]
        verificacion = datos["verificacion"]

        resultados[agente] = {
            "estado": resultado["estado"],
            "concluyente": verificacion["concluyente"],
            "contraejemplo": bool(
                verificacion["concluyente"]
                and verificacion["contraejemplo"]
            ),
            "discrepancias": verificacion["discrepancias"]
        }

    return {
        "grafo": grafo,
        "numero_aristas": len(grafo["aristas"]),
        "resultados": resultados,
        "informe_completo": informe
    }


if __name__ == "__main__":
    ejecutar_linea_base_aleatoria(semilla=11, presupuesto=1000)
