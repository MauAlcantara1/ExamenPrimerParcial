import json

def calculoAmplitud (grafo, informe):
    amplitud= 0.0

    for agente in ["B!", "U1", "A1"]:
        if agente not in informe: continue

        reporte = informe[agente]
        estado = reporte["resultado"].get("estado")
        esContraejemplo = reporte["verificacion"].get("contraejemplo",False)

        if esContraejemplo == True:
            amplitud += 1000
        elif estado == "solucion":
            amplitud += 3
        elif estado == "sin_solucion":
            amplitud +=1
        elif estado == "limite":
            amplitud -=5