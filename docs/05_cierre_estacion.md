# Ejercicio 5: Cierre de una estación (Impacto en la red)

## 1. ¿Qué problema resuelve el programa?
En redes de transporte, comunicaciones o logística, la eliminación temporal o definitiva de un nodo clave (una estación cerrada por reparaciones, un router caído) obliga al flujo a redirigirse por vías secundarias. Este programa modela la red de transporte, calcula las distancias más cortas (tiempos mínimos) entre orígenes y destinos, simula el cierre de una estación eliminando ese nodo de la red, y recalcula el impacto (tiempo adicional o desconexión) para un conjunto de rutas.

## 2. ¿Qué idea matemática usa?
- **Teoría de Grafos:** Se modela el problema utilizando un grafo ponderado no dirigido $G = (V, E, W)$, donde $V$ son las estaciones (vértices), $E$ son las conexiones (aristas) y $W: E \to \mathbb{R}^+$ es la función de peso (tiempo de viaje en minutos).
- **Algoritmo de Dijkstra:** Se utiliza para encontrar el camino más corto desde un nodo inicial hacia los demás, basándose en la relajación de las aristas y una cola de prioridad para garantizar el costo mínimo acumulado.
- **Modificación Topológica:** El cierre de la estación corresponde a la operación de subgrafo inducido $G' = G[V \setminus \{v_{cerrado}\}]$, es decir, la eliminación del vértice y todas sus aristas incidentes.

## 3. ¿Cómo se ejecuta?
Desde el directorio raíz del repositorio (`Programacion-Discreta/`):

1. **Ejecutar el programa de grafos (menú interactivo):**
   ```bash
   python src/grafos/cierre_estacion.py
   ```
2. **Ejecutar las pruebas unitarias:**
   ```bash
   python -m unittest tests/test_cierre.py
   ```

## 4. ¿Qué pruebas hicieron?
Se implementaron pruebas automatizadas (`tests/test_cierre.py`) verificando:
- **Dijkstra:** Validación del cálculo preciso del tiempo mínimo y la ruta correcta en el grafo intacto.
- **Desconexión Absoluta:** Si se cierra el único vértice que conecta un subgrafo, el sistema retorna `infinito` (representando la imposibilidad de llegar) y su estado cambia a `DESCONECTADO`.
- **Rutas Alternativas:** Se evaluó el caso `Banderas -> Centro` al cerrar `Ricaurte`. El sistema detecta correctamente que el tiempo pasa de 18 minutos (vía Ricaurte) a 40 minutos (ruta alterna vía Portal Sur).

## 5. ¿Qué limitaciones tiene la solución?
- Solo asume grafos estáticos; no contempla tiempos variables por hora pico, ni capacidades máximas de la estación.
- Si el grafo llega a ser gigantesco (como la red de Google Maps entera), Dijkstra nodo a nodo sería ineficiente y se requeriría $A^*$ o jerarquías de contracción (Contraction Hierarchies).

---

### Pregunta de Documentación

#### ¿Cuál vértice o arista cerraron y por qué ese cierre produce o no produce un impacto importante?
En nuestra demostración, cerramos el nodo **`Ricaurte`**. Este nodo funciona como un *puente o hub de transferencia* central.
- **Impacto importante:** Produce un impacto masivo. Rutas como `Banderas -> Centro`, que usualmente tomaban 18 minutos, aumentan drásticamente a 40 minutos porque los usuarios se ven obligados a dar una vuelta por el sur (`Portal Sur`). 
- **Cierres menos importantes:** Si hubiéramos cerrado una estación periférica (hoja del grafo) como `Portal_Norte`, no afectaría los tiempos de ninguna persona que no tuviera origen o destino específicamente en `Portal_Norte`. `Ricaurte`, al tener alta *intermediación* (Betweenness Centrality), afecta rutas de terceros.
