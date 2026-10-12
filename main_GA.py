import json
import random
import copy
import time
from pathlib import Path
from busqueda import evaluar, validar, heuristica, verificar
from grafos import CromosomaGrafo, AGENTES
from GA import calculoAptitud, selaccion, cruzar, mutar

def procGrafo(grafoDict, limite = 100):
    validar(grafoDict)
    informe = evaluar(grafoDict, limite_expansiones = limite)

    resultados = {}

    for agente in AGENTES:
        datos = informe[agente]
        resultados[agente] = {
            "estado": datos["resultado"]["estado"],
            "concluyente": datos["verificacion"]["concluyente"],
            "contraejemplo": bool(datos["verificacion"]["concluyente"] and datos["verificacion"]["contraejemplo"]),
            "discrepancias": datos["verificacion"]["discrepancias"]
        }

    return informe, resultados

def ejecutarGA(semilla, presupuesto):
    rng = random.Random(semilla)
    random.seed(semilla)

    print(f"Iniciando GA | semilla = {semilla} | presupuesto = {presupuesto}")

    carpeta = Path("resultadosGA")
    carpeta.mkdir(exist_ok=True)
    rutaDetalle = carpeta / f"GA_semilla_{semilla}_evaluaciones.jsonl"
    rutaResumen = carpeta / f"GA_semilla_{semilla}_resumen.json"

    evaluaciones = 0 
    tamPoblacion = 50
    poblacion = []
    contraejemplosEnc = {agente: [] for agente in AGENTES}
    tiempoIni = time.perf_counter()

    with rutaDetalle.open("w", encoding = "utf-8") as archivo:

        for _ in range(tamPoblacion):
            candidato = CromosomaGrafo()
            candidato.generar_grafo_aleatorio(rng)
            grafoIni = candidato.obtener_formato_profesor()
            poblacion.append({"grafo": grafoIni, "informe": None, "resultados": None, "fitness": None})

        generacion = 0

        while evaluaciones < presupuesto:

            for individuo in poblacion:

                if evaluaciones >= presupuesto: break

                if individuo["fitness"] is None:
                    informe, resultados = procGrafo(individuo["grafo"])
                    evaluaciones +=1

                    individuo["informe"] = informe
                    individuo["resultados"] = resultados

                    individuo["fitness"] = calculoAptitud(individuo["grafo"], informe)

                    archivo.write(json.dumps({
                        "evaluacion": evaluaciones,
                        "generacion": generacion,
                        "grafo": individuo["grafo"],
                        "informe": informe
                    }, ensure_ascii=False) + "\n")

                    for agente in AGENTES:
                        if resultados[agente]["contraejemplo"]:
                            if not contraejemplosEnc[agente]:
                                print(f"Contraejemplo en {agente} | Eval: {evaluaciones} | Gen: {generacion}")
                            contraejemplosEnc[agente].append({
                                "evaluacion": evaluaciones,
                                "grafo": individuo["grafo"],
                                "discrepancias": resultados[agente]["discrepancias"]
                            })
            if evaluaciones >= presupuesto: break

            poblacion.sort(key = lambda x: x["fitness"], reverse = True)
            nuevaPoblacion = copy.deepcopy(poblacion[:5])

            while len(nuevaPoblacion) < tamPoblacion:

                padre1 = selaccion(poblacion)
                padre2 = selaccion(poblacion)

                hijo = mutar(cruzar(padre1["grafo"], padre2["grafo"]))

                nuevaPoblacion.append({"grafo": hijo, "informe": None, "resultados": None, "fitness": None})

            poblacion = nuevaPoblacion
            generacion += 1

            if generacion % 5 == 0:
                print(f"Generacion {generacion} | Evaluaciones: {evaluaciones/presupuesto} | Mejor aptitud: {poblacion[0]['fitness']:.1f}")

    resumen = {
        "metodo": "algoritmo_genetico",
        "semilla": semilla,
        "generaciones_totales": generacion,
        "evaluaciones_consumidas": evaluaciones,
        "hallazgos_confirmados": {agente: len(contraejemplosEnc[agente]) for agente in AGENTES},
        "tiempo_segundos": round(time.perf_counter() - tiempoIni, 3),
        "contraejemplos_detalle": contraejemplosEnc
    }
    rutaResumen.write_text(json.dumps(resumen, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nTerminado. Resumen en {rutaResumen}")
                    
if __name__ == "__main__":
    semillasExigidas = [11, 22, 33, 44, 55]

    print("INICIANDO ALGORITMO GENETICO")
    print("=" * 50)
    for semillaActual in semillasExigidas:
        ejecutarGA(semilla=semillaActual, presupuesto=1000)
        print("-" * 50)
    print("Experimento Genetico Finalizado.")
