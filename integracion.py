
import random
import json

from grafos import CromosomaGrafo
from busqueda import validar, evaluar

random.seed(11)

candidato = CromosomaGrafo()
candidato.generar_grafo_aleatorio()

grafo = candidato.obtener_formato_profesor()

print(json.dumps(grafo, indent=2))

validar(grafo)
print("\nValidación aceptada")

informe = evaluar(grafo, limite_expansiones=100)

for agente, datos in informe.items():
    resultado = datos["resultado"]
    verificacion = datos["verificacion"]

    print(f"\nAgente: {agente}")
    print(f"Estado: {resultado['estado']}")
    print(f"Ruta: {resultado['ruta']}")
    print(f"Costo: {resultado['costo']}")
    print(f"Contraejemplo: {verificacion['contraejemplo']}")
    print(f"Concluyente: {verificacion['concluyente']}")
    print(f"Discrepancias: {verificacion['discrepancias']}")
