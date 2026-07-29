# Ejercicio 6: Coloreo de Grafos (Exámenes sin choques)

## 1. ¿Qué problema resuelve el programa?
El problema de calendarización o asignación de recursos limitados, donde ciertas actividades no pueden ocurrir simultáneamente. Específicamente, este programa ayuda a agrupar materias universitarias en "franjas horarias" (colores) para exámenes, de modo que si hay estudiantes inscritos en dos materias diferentes, ambas materias no se programen a la misma hora, evitando choques o solapamientos.

## 2. ¿Qué idea matemática usa?
El problema se modela matemáticamente como **Coloreo de Vértices** de un grafo. 
- Los vértices $V$ representan los cursos o materias.
- Las aristas $E$ representan los conflictos: existe la arista $\{u, v\}$ si y solo si los cursos $u$ y $v$ comparten estudiantes.
El objetivo es encontrar una función de asignación de colores $c: V \to \mathbb{N}$ tal que para toda arista $\{u, v\} \in E$, se cumpla que $c(u) \neq c(v)$.

Determinar el mínimo número de colores necesarios, conocido como el **Número Cromático** $\chi(G)$, es un problema NP-Completo. Por tanto, usamos el **Algoritmo Voraz (Greedy)**, específicamente complementado con la heurística de **Welsh-Powell** (ordenando los vértices de mayor a menor grado), lo que permite obtener una asignación de colores válida y cercanamente óptima en tiempo polinomial.

## 3. ¿Cómo se ejecuta?
Desde el directorio raíz del repositorio (`Programacion-Discreta/`):

1. **Ejecutar el script principal (CLI Interactivo):**
   ```bash
   python src/grafos/coloreo.py
   ```
2. **Ejecutar las pruebas unitarias:**
   ```bash
   python -m unittest tests/test_coloreo.py
   ```

## 4. ¿Qué pruebas se realizaron?
Se automatizaron varias pruebas en `tests/test_coloreo.py`:
- **Grafo de asignaturas (Obligatorio):** Se comprobó que el grafo de 11 materias de ejemplo arroja una asignación donde ninguna materia en conflicto comparte color, validado por la función auxiliar `verificar_coloreo`.
- **Grafos Completos ($K_n$):** Se verificó que un grafo completo de 4 nodos asigna exactamente 4 colores, ya que cada nodo choca con todos los demás.
- **Grafos Bipartitos (Estrella):** Se comprobó que un nodo central conectado a muchos nodos que no están conectados entre sí solo consume 2 colores (Centro de un color, todos los demás del otro).

## 5. Limitaciones de la solución
- **No garantiza el número cromático:** Al ser un algoritmo voraz, la cantidad total de colores puede variar dependiendo del orden en que se pasen los vértices, superando a veces el óptimo teórico.
- **Capacidades de aulas:** Este modelo básico no tiene en cuenta cuántas materias se pueden programar al mismo tiempo (ej. la disponibilidad de aulas físicas). 

---

### Preguntas conceptuales obligatorias

#### ¿Por qué el algoritmo voraz no siempre garantiza el menor número posible de colores?
Un algoritmo voraz toma la mejor decisión local en cada paso sin considerar el impacto global futuro. Si los nodos se procesan en un orden desfavorable, el algoritmo puede verse forzado a introducir un nuevo color simplemente porque los colores anteriores ya fueron bloqueados por vecinos procesados tempranamente de forma "inoportuna". 
Un ejemplo clásico es el **Grafo Corona** de $2n$ vértices. El número cromático de un grafo corona es 2 (es un grafo bipartito), pero si el algoritmo voraz procesa los vértices en un orden malicioso alternado (por ejemplo, emparejando vértices opuestos consecutivamente), puede terminar usando $n$ colores en lugar de 2.

#### ¿Por qué sí produce una asignación válida?
Produce una asignación válida porque en cada iteración del bucle, para el vértice actual $v$, se evalúan exhaustivamente todos los colores ya asignados a los vecinos adyacentes de $v$. El algoritmo avanza en el espectro de colores (0, 1, 2...) y selecciona el primer color que **no pertenezca** a ese conjunto de colores prohibidos por los vecinos. Por construcción, jamás le dará a $v$ el mismo color que ya tiene un vecino, cumpliendo estrictamente la definición matemática de coloreo de vértices en cada paso.
