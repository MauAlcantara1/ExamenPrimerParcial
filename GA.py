import random
import copy

def calculoAptitud (grafo, informe):
    aptitud = 0.0

    for agente in ["B!", "U1", "A1"]:
        if agente not in informe: continue

        reporte = informe[agente]
        estado = reporte["resultado"].get("estado")
        esContraejemplo = reporte["verificacion"].get("contraejemplo",False)

        if esContraejemplo == True:
            aptitud += 1000
        elif estado == "solucion":
            aptitud += 3
        elif estado == "sin_solucion":
            aptitud +=1
        elif estado == "limite":
            aptitud -=5

    cantAristas = len(grafo.get("aristas",[]))
    aptitud -= (cantAristas * 0.1)

    return aptitud

def cruzar (grafoP1, grafoP2):
    hijo = {"n": 6, "inicio": 0, "meta": 5, "aristas": []}

    hijo["inicio"] = random.choice([grafoP1["inicio"],grafoP2["inicio"]])
    hijo["meta"] = random.choice([grafoP1["meta"],grafoP2["meta"]])

    aristasP1 = {(u,v):costo for u, v, costo in grafoP1["aristas"]}
    aristasP2 = {(u,v):costo for u, v, costo in grafoP2["aristas"]}


    for u in range(6):
        for v in range(6):
            if u==v:
                continue

            if random.random() < 0.5:
                costo = aristasP1.get((u, v), 0)

            else:
                costo = aristasP2.get((u, v), 0)

            if costo > 0:
                hijo["aristas"].append([u, v, costo])

    return hijo


def mutar(grafo, probMutacion = 0.15):

    mutado = copy.deepcopy(grafo)

    """
    if random.random() < probMutacion:
        mutado["inicio"] = random.randint(0,5)

    if random.random() < probMutacion:
            mutado["meta"] = random.randint(0,5)
    """

    if random.random() < probMutacion:

        accion = random.choice(["agregar", "eliminar", "cambCosto"])

        if accion == "agregar":

            u, v = random.sample(range(6), 2)
            
            costo = random.randint(1, 9)

            if not any(a[0] == u and a[1] == v for a in mutado["aristas"]):
                mutado["aristas"].append([u, v, costo])

        elif accion == "eliminar" and len(mutado["aristas"]) > 0:

            idx = random.randrange(len(mutado["aristas"]))

            mutado["aristas"].pop(idx)

        elif accion == "cambCosto" and len(mutado["aristas"]) > 0:

            idx = random.randrange(len(mutado["aristas"]))

            mutado["aristas"][idx][2] = random.randint(1,9)

    return mutado


def selaccion(poblacion, k=3):

    participantes = random.sample(poblacion, k)

    ganador = max(participantes, key= lambda ind: ind["fitness"])

    return ganador

