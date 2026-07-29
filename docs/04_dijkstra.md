# Ejercicio 4: Ruta más corta con Dijkstra

## 1. ¿Qué problema resuelve el programa?
El algoritmo busca encontrar la ruta de menor costo (ruta óptima) entre dos puntos en una red o mapa representado por un grafo ponderado. En este ejercicio, el grafo modela una ciudad, donde los vértices son lugares (Portal, Centro, Universidad, etc.) y las aristas representan las calles que los conectan, siendo el peso de cada arista el tiempo en minutos necesario para recorrer esa calle.

## 2. ¿Qué idea matemática usa?
El algoritmo de Dijkstra se fundamenta en la teoría de optimización en grafos y utiliza el principio de **relajación de aristas**. Partiendo desde el nodo origen, el algoritmo mantiene una estimación de la distancia mínima hacia todos los demás nodos. Utilizando una estructura de cola de prioridad (min-heap), extrae repetidamente el vértice con la menor estimación actual y evalúa si es posible alcanzar a sus vecinos más rápido a través de él. Si es así, "relaja" la arista actualizando la distancia. 

Este enfoque de programación dinámica (tipo *Greedy* o voraz) garantiza que cuando un vértice se extrae del min-heap, su distancia mínima ha sido encontrada de manera definitiva.

## 3. ¿Cómo se ejecuta?
Desde el directorio raíz del repositorio (`Programacion-Discreta/`):

1. **Ejecutar el script principal (CLI Interactivo):**
   ```bash
   python src/grafos/dijkstra.py
   ```
2. **Ejecutar las pruebas unitarias:**
   ```bash
   python -m unittest tests/test_dijkstra.py
   ```

## 4. ¿Qué pruebas se realizaron?
Se incluyeron pruebas en `tests/test_dijkstra.py` para asegurar que:
- **Caminos estándar:** La búsqueda desde *Portal* hasta *Universidad* elija la ruta de menor costo matemático y no simplemente la que tiene menos saltos (encontrando la ruta Portal -> Calle26 -> Centro -> Parque -> Universidad).
- **Mismo origen y destino:** El costo para viajar al mismo lugar de inicio es `0`.
- **Grafos disconexos:** Nodos inalcanzables retornan distancia `infinito` y una lista vacía.
- **Manejo de excepciones:** Se probó que al introducir intencionalmente una arista con peso negativo el algoritmo lance una excepción de `ValueError` protegiéndose contra cálculos erróneos.

## 5. Limitaciones de la solución
- **Limitación en memoria:** El grafo está modelado como diccionarios en memoria. Para ciudades gigantescas (millones de nodos), requeriría optimizaciones con bases de datos gráficas.
- **No es bidireccional:** El algoritmo explora el grafo desde un solo lado de manera radial. Implementar *Bidirectional Dijkstra* o *A** (A-Star) sería mucho más eficiente para redes viales reales porque orienta la búsqueda gracias a una heurística geométrica.

---

### Preguntas conceptuales obligatorias

#### ¿Por qué Dijkstra necesita pesos no negativos?
El algoritmo de Dijkstra asume que, una vez que un nodo se extrae de la cola de prioridad, su distancia mínima ha sido encontrada definitivamente. Esto es cierto **solo si no existen pesos negativos**, porque al ir sumando pesos positivos, cualquier ruta futura que pase por otros nodos inevitablemente costará *más*. 
Si existieran pesos negativos, podríamos descubrir más adelante una ruta que reduzca el costo de un nodo que ya habíamos dado por "cerrado". Para lidiar con grafos que incluyen aristas de peso negativo se requiere el **Algoritmo de Bellman-Ford**. Adicionalmente, si el grafo contiene *ciclos de peso negativo*, el problema carece de solución finita, ya que se podría dar vueltas infinitamente en el ciclo para reducir el costo al infinito negativo.

#### ¿Qué significa matemáticamente que un camino sea "óptimo"?
En la teoría de grafos, dado un grafo $G = (V, E)$ y una función de peso $w: E \to \mathbb{R}^+$, un camino $P = (v_1, v_2, \dots, v_k)$ entre el nodo $v_1$ y el nodo $v_k$ es matemáticamente **óptimo** si la suma de los pesos de las aristas que lo componen:
$$ W(P) = \sum_{i=1}^{k-1} w(v_i, v_{i+1}) $$
es estrictamente menor o igual al peso $W(P')$ de cualquier otro camino posible $P'$ en el conjunto de todos los caminos simples entre $v_1$ y $v_k$.
