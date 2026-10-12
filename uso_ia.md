# Declaración de Uso de Inteligencia Artificial

**Proyecto:** Cazador Genético (Laboratorio de Contraejemplos)
**Equipo:** [Identificador de tu equipo / Nombres de los integrantes]

## 1. Herramienta y Modelo
Se utilizó asistencia de Inteligencia Artificial durante el desarrollo de este proyecto.
- **Herramienta:** Google Gemini
- **Modelo:** Gemini (Contexto de conversación continua)

## 2. Finalidad del uso
La IA fue utilizada estrictamente como "compañero de programación" (pair programming) y tutor conceptual para:
1. Desambiguar y aterrizar los requerimientos del proyecto (específicamente la diferencia entre el dominio evolutivo y la API de evaluación).
2. Diseñar la estructura de datos para la representación genética (Cromosoma).
3. Estructurar el esqueleto de la línea base aleatoria y el ciclo de guardado de evidencias.
4. Diseñar la lógica matemática detrás de la Función de Aptitud y los operadores genéticos.

## 3. Partes revisadas y verificaciones realizadas por el equipo
El equipo no integró código generado sin revisión previa. Las verificaciones principales fueron:
- **Representación matricial:** Se verificó matemáticamente que la matriz 6x6 propuesta por la IA previniera la creación de lazos (aristas hacia el mismo nodo) y se probó exitosamente el adaptador que la convierte a la lista de aristas que exige el evaluador.
- **Manejo de Incidencias:** Se revisó el código de evaluación y se realizaron pruebas forzando un límite bajo de expansiones (ej. `limite_expansiones=2`) para comprobar empíricamente que el sistema ignoraba los resultados de `"limite"` y `"error"`, cumpliendo estrictamente con el Requerimiento 5.
- **Comprobación Aislada:** Se validó que la función generadora de reportes ejecutara a los agentes de forma individual y extrajera correctamente la métrica de la `heuristica` exclusivamente para el agente A*, conforme al Requerimiento 11.

## 4. Observaciones relevantes
El uso de la IA aceleró significativamente la configuración del "boilerplate" (código repetitivo de lectura/escritura de archivos JSON y ciclos de evaluación). Sin embargo, el equipo fue responsable de orquestar los componentes, interpretar los resultados de B1, U1 y A1, y ensamblar el algoritmo genético final para asegurar la reproducibilidad exigida con las semillas 11, 22, 33, 44 y 55.

## 5. Registro acotado de consultas pertinentes
A continuación, un resumen de los prompts (consultas) clave utilizados para guiar la asistencia:

* *"Ayúdame a diseñar la representación del cromosoma para los grafos de 6 nodos. ¿Cómo estructuro la matriz y los nodos en Python?"*
* *"¿Cómo implemento el generador de grafos aleatorios (la línea base) que pide el requerimiento 6, usando esta misma estructura?"*
* *"Ayúdame a diseñar la Función de Aptitud (Requerimiento 3). ¿Cómo le doy una calificación numérica a un grafo basándome en el informe que devuelve el código del profesor?"*
* *"¿Cómo programamos ahora la Selección, el Cruzamiento y la Mutación (Requerimiento 2) para el Algoritmo Genético?"*
* *"De todos los grafos, necesito comprobar los errores que tenemos y no pasarlos mal. ¿Cómo hago una función fuera de la clase para comprobarlos?"*