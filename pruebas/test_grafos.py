
import contextlib
import io
import json
import os
import random
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from busqueda import evaluar, referencia, validar, verificar
from grafos import CromosomaGrafo, ejecutar_linea_base_aleatoria


AGENTES = ("B1", "U1", "A1")


def crear_grafo(aristas):
    return {"n": 6, "inicio": 0, "meta": 5, "aristas": aristas}


def resultado_controlado(estado, ruta=None, costo=None):
    return {"estado": estado, "ruta": ruta, "costo": costo,
            "expansiones": 0, "error": None}


def generar_muestra(semilla, cantidad=15):
    rng = random.Random(semilla)
    muestra = []
    for _ in range(cantidad):
        candidato = CromosomaGrafo()
        candidato.generar_grafo_aleatorio(rng)
        muestra.append(candidato.obtener_formato_profesor())
    return muestra


class PruebasRepresentacion(unittest.TestCase):
    def test_matriz_inicial_6x6_en_ceros(self):
        cromosoma = CromosomaGrafo()
        self.assertEqual(len(cromosoma.matriz), 6)
        self.assertTrue(all(len(fila) == 6 for fila in cromosoma.matriz))
        self.assertTrue(all(valor == 0 for fila in cromosoma.matriz for valor in fila))

    def test_adaptador_respeta_aristas_direccion_y_pesos(self):
        cromosoma = CromosomaGrafo()
        cromosoma.matriz[0][5] = 7
        cromosoma.matriz[3][4] = 2
        cromosoma.matriz[4][3] = 8
        copia = [fila[:] for fila in cromosoma.matriz]
        grafo = cromosoma.obtener_formato_profesor()
        self.assertEqual(grafo, crear_grafo([[0, 5, 7], [3, 4, 2], [4, 3, 8]]))
        self.assertEqual(cromosoma.matriz, copia, "Convertir no debe modificar el cromosoma")
        validar(grafo)

    def test_generador_preserva_dominio_en_100_intentos(self):
        rng = random.Random(123)
        for intento in range(100):
            with self.subTest(intento=intento):
                cromosoma = CromosomaGrafo()
                cromosoma.generar_grafo_aleatorio(rng)
                matriz = cromosoma.matriz
                self.assertEqual(len(matriz), 6)
                self.assertTrue(all(len(fila) == 6 for fila in matriz))
                self.assertTrue(all(matriz[i][i] == 0 for i in range(6)))
                self.assertTrue(all(type(peso) is int and 0 <= peso <= 9
                                    for fila in matriz for peso in fila))
                grafo = cromosoma.obtener_formato_profesor()
                self.assertLessEqual(len(grafo["aristas"]), 30)
                self.assertEqual(len({(u, v) for u, v, _ in grafo["aristas"]}),
                                 len(grafo["aristas"]))
                validar(grafo)

    def test_grafo_desconectado_tambien_es_valido(self):
        grafo = crear_grafo([[0, 1, 2], [1, 0, 3], [2, 4, 4]])
        validar(grafo)
        self.assertFalse(referencia(grafo)["existe_ruta"])
        for agente in AGENTES:
            datos = evaluar(grafo)[agente]
            self.assertEqual(datos["resultado"]["estado"], "sin_solucion")
            self.assertFalse(datos["verificacion"]["contraejemplo"])

    def test_misma_semilla_produce_mismos_candidatos(self):
        self.assertEqual(generar_muestra(11), generar_muestra(11))
        self.assertEqual(generar_muestra(44), generar_muestra(44))


class PruebasClasificacionSemantica(unittest.TestCase):
    """Casos controlados para verificar la interpretacion del contrato docente."""

    def test_dos_rutas_diferentes_pero_igual_de_buenas(self):
        grafo = crear_grafo([[0, 1, 2], [1, 5, 3],
                             [0, 2, 1], [2, 5, 4]])
        for agente in AGENTES:
            for ruta in ([0, 1, 5], [0, 2, 5]):
                with self.subTest(agente=agente, ruta=ruta):
                    v = verificar(agente, grafo,
                                 resultado_controlado("solucion", ruta, 5))
                    self.assertTrue(v["concluyente"])
                    self.assertFalse(v["contraejemplo"])
                    self.assertEqual(v["discrepancias"], [])

    def test_sin_solucion_real_no_es_un_fallo(self):
        grafo = crear_grafo([[0, 1, 3], [2, 5, 1]])
        for agente in AGENTES:
            v = verificar(agente, grafo, resultado_controlado("sin_solucion"))
            self.assertTrue(v["concluyente"])
            self.assertFalse(v["contraejemplo"])

    def test_falso_sin_solucion_si_hay_camino(self):
        grafo = crear_grafo([[0, 5, 4]])
        for agente in AGENTES:
            v = verificar(agente, grafo, resultado_controlado("sin_solucion"))
            self.assertTrue(v["concluyente"])
            self.assertTrue(v["contraejemplo"])
            self.assertIn("falso_sin_solucion", v["discrepancias"])

    def test_costo_declarado_incorrecto(self):
        grafo = crear_grafo([[0, 5, 4]])
        for agente in AGENTES:
            v = verificar(agente, grafo,
                         resultado_controlado("solucion", [0, 5], 99))
            self.assertTrue(v["concluyente"])
            self.assertTrue(v["contraejemplo"])
            self.assertIn("costo_incorrecto", v["discrepancias"])

    def test_bfs_minimiza_aristas_no_costo(self):
        grafo = crear_grafo([[0, 5, 9], [0, 1, 1], [1, 5, 1]])
        bfs = verificar("B1", grafo,
                       resultado_controlado("solucion", [0, 5], 9))
        ucs = verificar("U1", grafo,
                       resultado_controlado("solucion", [0, 5], 9))
        self.assertFalse(bfs["contraejemplo"])
        self.assertTrue(ucs["contraejemplo"])
        self.assertIn("no_optimo", ucs["discrepancias"])

    def test_ruta_con_mas_aristas_no_es_optima_para_bfs(self):
        grafo = crear_grafo([[0, 5, 9], [0, 1, 1], [1, 5, 1]])
        bfs = verificar("B1", grafo,
                       resultado_controlado("solucion", [0, 1, 5], 2))
        self.assertTrue(bfs["contraejemplo"])
        self.assertIn("no_optimo", bfs["discrepancias"])

    def test_limite_y_error_no_son_hallazgos_concluyentes(self):
        grafo = crear_grafo([[0, 5, 4]])
        for agente in AGENTES:
            for estado in ("limite", "error"):
                with self.subTest(agente=agente, estado=estado):
                    v = verificar(agente, grafo, resultado_controlado(estado))
                    self.assertFalse(v["concluyente"])
                    self.assertFalse(v["contraejemplo"])


class PruebasPresupuestoYReproducibilidad(unittest.TestCase):
    """Usa carpetas temporales, nunca resultados/ de las corridas oficiales."""

    @staticmethod
    def ejecutar_en_temporal(carpeta, semilla, presupuesto):
        origen = Path.cwd()
        try:
            os.chdir(carpeta)
            with contextlib.redirect_stdout(io.StringIO()):
                with mock.patch("grafos.evaluar", wraps=evaluar) as evaluador:
                    resumen = ejecutar_linea_base_aleatoria(
                        semilla=semilla, presupuesto=presupuesto,
                        limite_expansiones=100,
                    )
            prefijo = f"aleatoria_semilla_{semilla}"
            detalle = Path("resultados") / f"{prefijo}_evaluaciones.jsonl"
            archivo_resumen = Path("resultados") / f"{prefijo}_resumen.json"
            lineas = [json.loads(linea) for linea in detalle.read_text(encoding="utf-8").splitlines()]
            resumen_disco = json.loads(archivo_resumen.read_text(encoding="utf-8"))
            return resumen, resumen_disco, lineas, evaluador.call_count
        finally:
            os.chdir(origen)

    def test_presupuesto_exactamente_12_evaluaciones(self):
        with tempfile.TemporaryDirectory() as temporal:
            resumen, en_disco, registros, llamadas = self.ejecutar_en_temporal(
                temporal, 22, 12,
            )
        self.assertEqual(llamadas, 12, "Una llamada a evaluar por candidato")
        self.assertEqual(len(registros), 12)
        self.assertEqual(resumen["evaluaciones_consumidas"], 12)
        self.assertEqual(en_disco["evaluaciones_consumidas"], 12)
        self.assertEqual([r["evaluacion"] for r in registros], list(range(1, 13)))
        self.assertEqual(resumen["progreso"][-1]["evaluaciones"], 12)
        for registro in registros:
            validar(registro["grafo"])
            self.assertEqual(set(registro["informe"]), set(AGENTES))
            for agente in AGENTES:
                self.assertIn("resultado", registro["informe"][agente])
                self.assertIn("verificacion", registro["informe"][agente])

    def test_linea_base_reproducible_con_semilla_fija(self):
        with tempfile.TemporaryDirectory() as dir1, tempfile.TemporaryDirectory() as dir2:
            resumen1, disco1, registros1, llamadas1 = self.ejecutar_en_temporal(dir1, 44, 15)
            resumen2, disco2, registros2, llamadas2 = self.ejecutar_en_temporal(dir2, 44, 15)
        self.assertEqual((llamadas1, llamadas2), (15, 15))
        self.assertEqual(registros1, registros2)
        self.assertEqual(resumen1["semilla"], resumen2["semilla"])
        for resumen in (disco1, disco2):
            resumen.pop("tiempo_segundos", None) 
        self.assertEqual(disco1, disco2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
