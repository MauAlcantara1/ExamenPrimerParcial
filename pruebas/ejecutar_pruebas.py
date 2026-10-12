
import datetime
import platform
import subprocess
import sys
from pathlib import Path


def main():
    base = Path(__file__).resolve().parent
    evidencia = base / "evidencia_pruebas.txt"
    comando = [sys.executable, "-m", "unittest", "-v", "test_contrato", "test_grafos"]
    try:
        proceso = subprocess.run(
            comando, cwd=base, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=120,
            check=False,
        )
        salida = (proceso.stdout or "") + (proceso.stderr or "")
        encabezado = (
            "EVIDENCIA DE PRUEBAS AUTOMATIZADAS - EJECUCION REAL\n"
            f"Fecha local: {datetime.datetime.now().astimezone().isoformat(timespec='seconds')}\n"
            f"Python: {platform.python_version()}\n"
            f"Plataforma: {platform.platform()}\n"
            f"Carpeta: {base}\n"
            "Comando: python -m unittest -v test_contrato test_grafos\n"
            f"Codigo de salida: {proceso.returncode}\n\n"
        )
        evidencia.write_text(encabezado + salida + "\n", encoding="utf-8")
        print(encabezado + salida)
        print(f"Evidencia guardada en: {evidencia}")
        return proceso.returncode
    except subprocess.TimeoutExpired:
        evidencia.write_text(
            "Ejecucion interrumpida por superar 120 segundos.\n"
            "No se acredita una ejecucion exitosa. Investigar el motivo.\n",
            encoding="utf-8",
        )
        print(f"Las pruebas excedieron el tiempo; revisar: {evidencia}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
