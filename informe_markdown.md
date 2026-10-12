
## 1. Objetivo y formulación del problema 

El proyecto busca desarrollar un sistema capaz de generar grafos dirigidos y ponderados de seis nodos, respetando las restricciones establecidas.

Los grafos generados se utilizan como casos de prueba para evaluar el comportamiento de tres algoritmos de búsqueda proporcionados por el profesor: BFS, UCS y A*. Mediante un evaluador se comprueba si sus resultados cumplen con los criterios correspondientes.

El algoritmo genético utiliza esta información para valorar los grafos y generar nuevos candidatos mediante un proceso evolutivo. Finalmente, se comparan los resultados obtenidos con los de una búsqueda aleatoria, utilizando el mismo presupuesto de evaluaciones para analizar su capacidad de encontrar contraejemplos.


## 2. Representación y validez de los grafos 


Se eligió una matriz de adyacencia de 6 × 6 porque el sistema trabaja con seis nodos y esta representación permite almacenar sus conexiones y pesos de manera sencilla. Posteriormente, la matriz se transforma al formato requerido por el evaluador del profesor, compatible con JSON.

Los grafos se generan aleatoriamente, con una probabilidad del 30 % de crear cada arista dirigida y asignando pesos enteros entre 1 y 9. El valor cero representa la ausencia de una conexión. Además, se evita la formación de lazos, es decir, conexiones de un nodo consigo mismo.

Finalmente, se utiliza la función `validar()` del paquete docente para comprobar que los grafos generados cumplan las restricciones establecidas.

## 3. Aptitud y operadores del algoritmo genético



## 4. Línea base aleatoria y reproducibilidad 

La línea base aleatoria genera grafos de manera independiente, utilizando una probabilidad del 30 % de crear una arista entre cada pareja de nodos distintos. Cuando se genera una conexión, se le asigna un peso entero aleatorio entre 1 y 9.

Para garantizar la reproducibilidad, se utiliza random.Random(semilla), permitiendo obtener los mismos grafos al repetir una ejecución con la misma semilla. Las semillas establecidas son 11, 22, 33, 44 y 55.

Cada ejecución contempla 1,000 grafos, evaluados mediante los algoritmos B1, U1 y A1, con un límite de 100 expansiones por agente.

Los resultados individuales se almacenan en archivos .jsonl, mientras que los archivos _resumen.json contienen la configuración, el progreso, los primeros contraejemplos detectados, las incidencias y el tiempo total de ejecución

## 5. Evaluación semántica y factibilidad 

Para evaluar los grafos generados, utilizamos la función evaluar() del paquete docente, que ejecuta los algoritmos B1 (BFS), U1 (UCS) y A1 (A*) y verifica sus resultados.

Cada algoritmo tiene diferentes criterios de optimalidad. BFS busca minimizar la cantidad de aristas, mientras que UCS y A* buscan minimizar el costo acumulado. Por ello, una ruta diferente no necesariamente representa un error si cumple con el criterio correspondiente.

Para identificar contraejemplos, revisamos que los resultados tengan concluyente: true y contraejemplo: true. También diferenciamos los estados sin_solucion, limite y error, evitando considerarlos equivalentes.

Durante las evaluaciones encontramos y reprodujimos tres contraejemplos representativos, correspondientes a B1, U1 y A1, en los que se detectaron incumplimientos de optimalidad.

## 6. Resultados y comparación experimental

Se realizaron cinco ejecuciones de búsqueda aleatoria utilizando las semillas 11, 22, 33, 44 y 55, con un presupuesto de 1,000 grafos por ejecución. En total, se analizaron 5,000 grafos diferentes mediante los tres algoritmos proporcionados por el profesor.

Los resultados mostraron 52 contraejemplos confirmados para B1, 147 para U1 y 187 para A1. Debido a que un mismo grafo puede revelar errores en varios algoritmos, estas cantidades no representan grafos únicos. En total, 233 grafos presentaron al menos un incumplimiento confirmado.

Los tres algoritmos presentaron contraejemplos en las cinco semillas. La mediana de la primera detección fue de 188 evaluaciones para B1 y de 7 para U1 y A1.

Durante las ejecuciones no se registraron errores de ejecución ni interrupciones por el límite de expansiones. El tiempo acumulado registrado fue de 3.139 segundos.

Estos resultados establecen una referencia para comparar el algoritmo genético con la búsqueda aleatoria bajo el mismo presupuesto. La comparación definitiva se incorporará una vez que estén disponibles las cinco ejecuciones del método genético.

## 7. Tres contraejemplos representativos 

Los tres contraejemplos identificados para los algoritmos B1 (BFS), U1 (UCS) y A1 (A*), junto con sus grafos, rutas, costos, representaciones visuales y explicaciones de los incumplimientos, se encuentran documentados en el archivo Word Comprobables.

## 7. Limitaciones y reflexión conceptual

El proyecto se limita a grafos sintéticos de seis nodos, con una probabilidad inicial de conexión del 30 %, cinco semillas y un presupuesto fijo de 1,000 evaluaciones por ejecución. Estas condiciones limitan el alcance de los resultados, ya que no encontrar un error no significa que un algoritmo sea correcto en todos los casos.

También es importante distinguir dos procesos: el algoritmo genético busca evolucionar grafos que permitan descubrir errores, mientras que BFS, UCS y A* buscan rutas dentro de esos grafos. A diferencia de los enfoques lógicos basados en reglas o del aprendizaje basado en datos, nuestro proyecto utiliza un enfoque evolutivo para optimizar las entradas de prueba.

McCarthy propuso estudiar cómo las máquinas podían simular capacidades inteligentes. Posteriormente, Turing abordó la inteligencia mediante el juego de imitación, mientras que Searle cuestionó si manipular símbolos implica comprenderlos. Por ello, encontrar errores o generar buenas pruebas no demuestra que nuestro sistema tenga comprensión.

https://www-formal.stanford.edu/jmc/history/dartmouth.pdf
https://academic.oup.com/mind/article/LIX/236/433/986238
https://zoo.cs.yale.edu/classes/cs458/materials/minds-brains-and-programs.pdf