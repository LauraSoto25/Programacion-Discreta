"""
Módulo para el Cierre de Estación y cálculo de impacto en la red (Grafos).
Matemáticas Discretas I - Taller 3

Implementa un grafo ponderado, el algoritmo de Dijkstra para rutas más cortas,
y simula el impacto de eliminar un vértice (cerrar una estación) sobre varias rutas.
"""

import heapq
from typing import Dict, List, Tuple, Any

class Grafo:
    def __init__(self):
        self.adj: Dict[str, Dict[str, float]] = {}

    def agregar_vertice(self, v: str):
        if v not in self.adj:
            self.adj[v] = {}

    def agregar_arista(self, u: str, v: str, peso: float):
        self.agregar_vertice(u)
        self.agregar_vertice(v)
        self.adj[u][v] = peso
        self.adj[v][u] = peso  # Grafo no dirigido

    def eliminar_vertice(self, v: str):
        """Elimina un vértice y todas las aristas conectadas a él."""
        if v in self.adj:
            vecinos = list(self.adj[v].keys())
            for vecino in vecinos:
                if v in self.adj[vecino]:
                    del self.adj[vecino][v]
            del self.adj[v]

    def dijkstra(self, inicio: str, destino: str) -> Tuple[float, List[str]]:
        """
        Algoritmo de Dijkstra para encontrar la distancia y ruta más corta.
        Retorna (distancia, ruta). Si no hay camino, retorna (float('inf'), []).
        """
        if inicio not in self.adj or destino not in self.adj:
            return float('inf'), []

        distancias = {nodo: float('inf') for nodo in self.adj}
        distancias[inicio] = 0
        padres = {nodo: None for nodo in self.adj}
        
        # Cola de prioridad: (distancia_acumulada, nodo_actual)
        pq = [(0, inicio)]

        while pq:
            dist_actual, nodo_actual = heapq.heappop(pq)

            # Si ya llegamos al destino, podemos detenernos temprano (opcional pero eficiente)
            if nodo_actual == destino:
                break

            # Si encontramos una distancia mayor en la cola que la ya registrada, la ignoramos
            if dist_actual > distancias[nodo_actual]:
                continue

            for vecino, peso in self.adj[nodo_actual].items():
                nueva_distancia = dist_actual + peso
                
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    padres[vecino] = nodo_actual
                    heapq.heappush(pq, (nueva_distancia, vecino))

        # Reconstruir la ruta
        if distancias[destino] == float('inf'):
            return float('inf'), []
            
        ruta = []
        actual = destino
        while actual is not None:
            ruta.append(actual)
            actual = padres[actual]
        ruta.reverse()
        
        return distancias[destino], ruta


def construir_grafo_prueba() -> Grafo:
    """Construye un grafo de una red de transporte con 9 nodos y 12 aristas."""
    g = Grafo()
    aristas = [
        ("Portal_Norte", "Calle_100", 10),
        ("Calle_100", "Calle_72", 8),
        ("Calle_72", "Centro", 15),
        ("Calle_72", "Ricaurte", 12),
        ("Centro", "Museo_Oro", 5),
        ("Centro", "Portal_Sur", 25),
        ("Ricaurte", "Centro", 8),
        ("Ricaurte", "Banderas", 10),
        ("Banderas", "Portal_Americas", 8),
        ("Calle_100", "Ricaurte", 20),
        ("Portal_Sur", "Banderas", 15),
        ("Museo_Oro", "Portal_Sur", 20)
    ]
    for u, v, peso in aristas:
        g.agregar_arista(u, v, peso)
    return g


def simular_cierre(grafo_original: Grafo, estacion_cerrada: str, pares: List[Tuple[str, str]]) -> List[Dict[str, Any]]:
    """
    Calcula las distancias antes y después del cierre, y reporta el impacto.
    Retorna una lista con el reporte por cada par origen-destino.
    """
    import copy
    
    # 1. Medir antes del cierre
    resultados = []
    for origen, destino in pares:
        dist_antes, ruta_antes = grafo_original.dijkstra(origen, destino)
        resultados.append({
            "origen": origen,
            "destino": destino,
            "dist_antes": dist_antes,
            "ruta_antes": ruta_antes
        })
        
    # 2. Cerrar la estación
    grafo_modificado = copy.deepcopy(grafo_original)
    grafo_modificado.eliminar_vertice(estacion_cerrada)
    
    # 3. Medir después del cierre y calcular diferencia
    for res in resultados:
        origen = res["origen"]
        destino = res["destino"]
        
        # Si cerraron el origen o el destino
        if origen == estacion_cerrada or destino == estacion_cerrada:
            dist_despues = float('inf')
            ruta_despues = []
        else:
            dist_despues, ruta_despues = grafo_modificado.dijkstra(origen, destino)
            
        res["dist_despues"] = dist_despues
        res["ruta_despues"] = ruta_despues
        
        if dist_despues == float('inf') and res["dist_antes"] != float('inf'):
            res["estado"] = "DESCONECTADO"
            res["diferencia"] = float('inf')
        elif dist_despues == float('inf') and res["dist_antes"] == float('inf'):
            res["estado"] = "YA ESTABA DESCONECTADO"
            res["diferencia"] = 0
        else:
            dif = dist_despues - res["dist_antes"]
            res["diferencia"] = dif
            if dif > 0:
                res["estado"] = "AUMENTÓ"
            elif dif < 0:
                res["estado"] = "DISMINUYÓ"  # Rarísimo en grafos no dirigidos quitando nodos
            else:
                res["estado"] = "IGUAL"
                
    return resultados


def imprimir_tabla(reporte: List[Dict[str, Any]], estacion_cerrada: str):
    """Imprime el resultado en formato de tabla en la consola."""
    print(f"\n--- REPORTE DE IMPACTO POR CIERRE DE: {estacion_cerrada.upper()} ---\n")
    print(f"{'Origen':<16} | {'Destino':<16} | {'Antes':<6} | {'Después':<7} | {'Dif.':<6} | {'Estado'}")
    print("-" * 75)
    
    for r in reporte:
        d_antes = f"{r['dist_antes']}" if r['dist_antes'] != float('inf') else "Inf"
        d_despues = f"{r['dist_despues']}" if r['dist_despues'] != float('inf') else "Inf"
        dif = f"+{r['diferencia']}" if r['diferencia'] != float('inf') and r['diferencia'] > 0 else ( "Inf" if r['diferencia'] == float('inf') else f"{r['diferencia']}")
        
        print(f"{r['origen']:<16} | {r['destino']:<16} | {d_antes:<6} | {d_despues:<7} | {dif:<6} | {r['estado']}")
    print("-" * 75)


if __name__ == "__main__":
    grafo_actual = construir_grafo_prueba()
    
    # Pares de prueba predefinidos
    pares_prueba = [
        ("Portal_Norte", "Portal_Sur"),
        ("Calle_100", "Banderas"),
        ("Portal_Americas", "Centro"),
        ("Calle_72", "Portal_Sur"),
        ("Banderas", "Centro")
    ]

    while True:
        print("\n=== CIERRE DE UNA ESTACIÓN (Impacto en la red) ===")
        print("1. Ver nodos disponibles en la red de prueba")
        print("2. Simular cierre de estación (Elegir estación a cerrar)")
        print("3. Ver demostración por defecto (Cerrar 'Ricaurte')")
        print("0. Salir")
        
        try:
            opcion = input("\nElige una opción (0-3): ").strip()
            
            if opcion == '1':
                nodos = list(grafo_actual.adj.keys())
                print(f"\nEstaciones en la red ({len(nodos)}):")
                for n in nodos:
                    print(f" - {n}")
                    
            elif opcion == '2':
                nodos = list(grafo_actual.adj.keys())
                estacion = input("\nEscribe exactamente el nombre de la estación a cerrar: ").strip()
                if estacion not in nodos:
                    print(f"\n[!] La estación '{estacion}' no existe en la red.")
                    continue
                
                print(f"\nCalculando rutas para 5 pares origen-destino cerrando '{estacion}'...")
                reporte = simular_cierre(grafo_actual, estacion, pares_prueba)
                imprimir_tabla(reporte, estacion)
                
            elif opcion == '3':
                estacion = "Ricaurte"
                print(f"\nCalculando rutas para 5 pares origen-destino cerrando '{estacion}'...")
                reporte = simular_cierre(grafo_actual, estacion, pares_prueba)
                imprimir_tabla(reporte, estacion)
                
                print("\n[Detalle de rutas antes vs después para el par Banderas -> Centro]")
                detalle = next(r for r in reporte if r["origen"] == "Banderas" and r["destino"] == "Centro")
                print(f"Ruta Antes   : {' -> '.join(detalle['ruta_antes'])} (Tiempo: {detalle['dist_antes']})")
                print(f"Ruta Después : {' -> '.join(detalle['ruta_despues'])} (Tiempo: {detalle['dist_despues']})")
                
            elif opcion == '0':
                print("\nSaliendo del programa...")
                break
            else:
                print("\n[!] Opción no válida. Inténtalo de nuevo.")
                
        except KeyboardInterrupt:
            print("\n[!] Operación cancelada por el usuario. Saliendo...")
            break
