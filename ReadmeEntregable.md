# Cazador genético de contraejemplos

Proyecto de evaluación de agentes de búsqueda B1 (BFS), U1 (UCS) y A1 (A*) mediante grafos dirigidos ponderados. El equipo desarrolla un generador de grafos y una línea base aleatoria; el algoritmo genético se encuentra en integración.

## INTEGRANTES

- Alcantara Cruz Donovan Amaury
- Martin Gabriel Ramirez Hilario
- Carlos Alberto 

## Comandos para correr todo

python --version
python -m unittest -v test_contrato
python integracion.py
python -m busqueda ejemplo.json --limite 100
python grafos.py

## Comandos para correr todo

Abrir la terminal de VS Code en la carpeta `estudiantes/`, donde están `grafos.py`, `integracion.py` y `test_contrato.py`.

```powershell
python --version
python -m unittest -v test_contrato
python integracion.py
python -m busqueda ejemplo.json --limite 100
python grafos.py
```

### ¿Qué hace cada comando?

| Comando | Propósito |
|---|---|
| `python --version` | Consultar la versión de Python utilizada. |
| `python -m unittest -v test_contrato` | Ejecutar las pruebas de contrato suministradas por el profesor. |
| `python integracion.py` | Generar un grafo de prueba, validarlo y consultar los resultados de B1, U1 y A1. |
| `python -m busqueda ejemplo.json --limite 100` | Ejecutar el ejemplo incluido en el paquete docente con límite de 100 expansiones. |
| `python grafos.py` | Ejecutar la línea base aleatoria actual: 1,000 evaluaciones con semilla 11. |

## Versión 3.14.6

- **Lenguaje:** Python 3.14.6 (versión utilizada por el equipo).
- **Paquete docente:** `busqueda`, versión 1.0.0, sin modificaciones.
- **Dependencias del código propio mostrado:** biblioteca estándar de Python y paquete docente.

## Estructura actual del proyecto

```text
estudiantes/
├── busqueda/              # Paquete docente (no modificar)
├── resultados/            # Archivos JSON/JSONL de las ejecuciones
├── ejemplo.json           # Grafo de ejemplo del profesor
├── grafos.py              # Cromosomas y búsqueda aleatoria
├── integracion.py         # Prueba individual de integración
├── README.md              # Estas instrucciones
├── ReadmeEntregable.md    # Notas de entrega del equipo
└── test_contrato.py       # Pruebas docentes
```

La carpeta `__pycache__/` puede generarse automáticamente y no es necesaria para reproducir las pruebas.

## Resultados actuales

El módulo `grafos.py` permite realizar ejecuciones independientes de la búsqueda aleatoria utilizando las cinco semillas establecidas para el experimento:

**11, 22, 33, 44 y 55.**

Cada semilla genera y evalúa 1,000 grafos dirigidos ponderados, utilizando el paquete docente para ejecutar y verificar los agentes B1 (BFS), U1 (UCS) y A1 (A*).

En total, la línea base aleatoria comprende **5,000 evaluaciones**, distribuidas en cinco ejecuciones independientes.

Los resultados se almacenan en la carpeta `resultados/`. Si se conserva la nomenclatura actual de `grafos.py`, la estructura es:

```text
resultados/
├── aleatoria_semilla_11_evaluaciones.jsonl
├── aleatoria_semilla_11_resumen.json
├── aleatoria_semilla_22_evaluaciones.jsonl
├── aleatoria_semilla_22_resumen.json
├── aleatoria_semilla_33_evaluaciones.jsonl
├── aleatoria_semilla_33_resumen.json
├── aleatoria_semilla_44_evaluaciones.jsonl
├── aleatoria_semilla_44_resumen.json
├── aleatoria_semilla_55_evaluaciones.jsonl
└── aleatoria_semilla_55_resumen.json
```

Cada archivo `.jsonl` contiene los grafos generados y los resultados completos de B1, U1 y A1 por evaluación.

Cada archivo `_resumen.json` contiene la configuración experimental, cantidad de evaluaciones, grafos distintos, progreso, hallazgos reportados, incidencias y tiempo de ejecución.

Estas ejecuciones constituyen la línea base para comparar posteriormente los resultados obtenidos mediante el algoritmo genético.

Las evaluaciones del algoritmo genético se almacenarán por separado para evitar confundir ambos métodos.