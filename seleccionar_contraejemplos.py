
import json
from pathlib import Path

from busqueda import validar, evaluar, heuristica

SEMILLAS = [11, 22, 33, 44, 55]
AGENTES = ["B1", "U1", "A1"]

CARPETA_RESULTADOS = Path("resultados")
CARPETA_SALIDA = Path("contraejemplos/preliminares")
CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)


def explicar_defecto(agente, resultado, verificacion):
    discrepancias = verificacion["discrepancias"]
    referencia = verificacion["referencia"]

    if "no_optimo" in discrepancias:
        if agente == "B1":
            ruta = resultado["ruta"]
            aristas_obtenidas = len(ruta) - 1
            aristas_minimas = referencia["distancia_minima_aristas"]

            return (
                f"B1 devolvió una ruta con {aristas_obtenidas} "
                f"aristas, pero la referencia establece "
                f"un mínimo de {aristas_minimas}."
            )

        return (
            f"{agente} devolvió un costo de {resultado['costo']}, "
            f"pero el costo mínimo es {referencia['costo_minimo']}."
        )

    return (
        "El verificador confirmó las discrepancias: "
        + ", ".join(discrepancias)
        + ". El equipo debe completar la explicación técnica."
    )


grafos_seleccionados = set()
indice = []

for agente in AGENTES:
    encontrado = False

    for semilla in SEMILLAS:
        archivo = (
            CARPETA_RESULTADOS
            / f"aleatoria_semilla_{semilla}_evaluaciones.jsonl"
        )

        if not archivo.exists():
            print(f"No existe: {archivo}")
            continue

        with archivo.open("r", encoding="utf-8") as f:
            for linea in f:
                registro = json.loads(linea)

                datos_guardados = registro["informe"][agente]
                verificacion = datos_guardados["verificacion"]

                # Solo considerar defectos semánticos confirmados
                if not (
                    verificacion["concluyente"]
                    and verificacion["contraejemplo"]
                ):
                    continue

                grafo = registro["grafo"]

                # Evitar entregar el mismo grafo dos veces
                clave = json.dumps(
                    grafo,
                    sort_keys=True,
                    separators=(",", ":")
                )

                if clave in grafos_seleccionados:
                    continue

                # Reproducir el caso fuera del experimento
                validar(grafo)
                nuevo = evaluar(
                    grafo,
                    limite_expansiones=100
                )[agente]

                # Comprobar que el resultado sigue siendo el mismo
                if nuevo != datos_guardados:
                    print(
                        f"El caso {agente}, semilla {semilla}, "
                        f"evaluación {registro['evaluacion']} "
                        f"no se reprodujo exactamente."
                    )
                    continue

                if not (
                    nuevo["verificacion"]["concluyente"]
                    and nuevo["verificacion"]["contraejemplo"]
                ):
                    continue

                resultado = nuevo["resultado"]
                diagnostico = nuevo["verificacion"]

                evidencia = {
                    "metodo": "aleatoria",
                    "semilla": semilla,
                    "numero_evaluacion": registro["evaluacion"],
                    "agente": agente,
                    "grafo": grafo,
                    "resultado_referencia": diagnostico["referencia"],
                    "resultado_objetivo": resultado,
                    "discrepancias": diagnostico["discrepancias"],
                    "explicacion": explicar_defecto(
                        agente, resultado, diagnostico
                    ),
                    "reproduccion": "Coincide con el registro original"
                }

                if agente == "A1":
                    evidencia["heuristica_utilizada"] = heuristica(grafo)

                nombre = (
                    f"{agente}_semilla_{semilla}_"
                    f"eval_{registro['evaluacion']:04d}.json"
                )

                destino = CARPETA_SALIDA / nombre

                destino.write_text(
                    json.dumps(evidencia, indent=2, ensure_ascii=False),
                    encoding="utf-8"
                )

                grafos_seleccionados.add(clave)

                indice.append({
                    "archivo": nombre,
                    "agente": agente,
                    "semilla": semilla,
                    "evaluacion": registro["evaluacion"],
                    "discrepancias": diagnostico["discrepancias"]
                })

                print(f"Reproducido y guardado: {nombre}")
                encontrado = True
                break

        if encontrado:
            break

    if not encontrado:
        print(f"{agente}: no se seleccionó un caso reproducible")

# Guardar el índice de los candidatos seleccionados
ruta_indice = CARPETA_SALIDA / "indice_preliminar.json"

ruta_indice.write_text(
    json.dumps(indice, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(f"\nTotal de casos seleccionados: {len(indice)}")
print(f"Carpeta: {CARPETA_SALIDA}")
