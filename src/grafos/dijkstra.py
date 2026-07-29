"""
Algoritmo de Dijkstra para encontrar la ruta más corta en un grafo ponderado.
Ejercicio 4 del Taller 3.
"""

import heapq
from typing import Dict, List, Tuple, Optional

# Definición de tipos para el grafo
Grafo = Dict[str, Dict[str, float]]

def dijkstra(grafo: Grafo, origen: str, destino: str) -> Tuple[float, List[str]]:
    """
    Encuentra la ruta más corta entre un nodo de origen y uno de destino usando Dijkstra.
    
    Parámetros:
        grafo (Grafo): Diccionario de diccionarios representando las adyacencias y pesos.
        origen (str): Nodo inicial.
        destino (str): Nodo final.
        
    Retorna:
        Tuple[float, List[str]]: Una tupla que contiene la distancia total y 
        la lista de nodos que conforman el camino óptimo. Si no hay ruta, 
        la distancia será infinita y la lista estará vacía.
        
    Excepciones:
        ValueError: Si algún peso es negativo, ya que Dijkstra no lo soporta.
    """
    if origen not in grafo or destino not in grafo:
        return float('inf'), []
        
    # Inicializar distancias al infinito
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[origen] = 0.0
    
    # Diccionario para reconstruir el camino
    predecesores: Dict[str, Optional[str]] = {nodo: None for nodo in grafo}
    
    # Cola de prioridad (min-heap) para explorar los nodos más cercanos primero
    # Almacena tuplas (distancia_acumulada, nodo)
    pq = [(0.0, origen)]
    
    while pq:
        distancia_actual, nodo_actual = heapq.heappop(pq)
        
        # Si llegamos al destino, podemos detenernos anticipadamente 
        # (ya que los pesos son todos positivos)
        if nodo_actual == destino:
            break
            
        # Si encontramos en la cola un nodo que ya fue procesado con una ruta más corta, lo ignoramos
        if distancia_actual > distancias[nodo_actual]:
            continue
            
        # Explorar vecinos
        for vecino, peso in grafo[nodo_actual].items():
            if peso < 0:
                raise ValueError(f"Dijkstra no soporta pesos negativos (arista {nodo_actual}-{vecino} tiene peso {peso})")
                
            distancia_alternativa = distancia_actual + peso
            
            # Si encontramos un camino más corto, relajamos la arista
            if distancia_alternativa < distancias[vecino]:
                distancias[vecino] = distancia_alternativa
                predecesores[vecino] = nodo_actual
                heapq.heappush(pq, (distancia_alternativa, vecino))
                
    # Reconstruir la ruta
    ruta = []
    nodo = destino
    
    # Si la distancia al destino es infinita, es inalcanzable
    if distancias[destino] == float('inf'):
        return float('inf'), []
        
    while nodo is not None:
        ruta.insert(0, nodo)
        nodo = predecesores[nodo]
        
    return distancias[destino], ruta


# Grafo de prueba (Ciudad)
CIUDAD: Grafo = {
    "Portal": {"Calle26": 5, "Centro": 10},
    "Calle26": {"Portal": 5, "Centro": 2, "Museo": 6},
    "Centro": {"Portal": 10, "Calle26": 2, "Biblioteca": 3, "Parque": 7},
    "Museo": {"Calle26": 6, "Universidad": 8, "Biblioteca": 1},
    "Biblioteca": {"Centro": 3, "Museo": 1, "Estadio": 4},
    "Parque": {"Centro": 7, "Universidad": 2},
    "Universidad": {"Museo": 8, "Parque": 2, "Estadio": 3},
    "Estadio": {"Biblioteca": 4, "Universidad": 3}
}


if __name__ == "__main__":
    while True:
        print("\n=== RUTA MÁS CORTA (DIJKSTRA) ===")
        print("1. Buscar ruta en la ciudad de prueba")
        print("2. Ver todas las conexiones de la ciudad")
        print("0. Salir")
        
        opcion = input("\nElige una opción (0-2): ").strip()
        
        if opcion == '1':
            print("\nLugares disponibles:", ", ".join(CIUDAD.keys()))
            origen = input("Ingresa el lugar de origen: ").strip()
            destino = input("Ingresa el lugar de destino: ").strip()
            
            if origen not in CIUDAD or destino not in CIUDAD:
                print("\n[!] Error: Uno o ambos lugares no existen en la ciudad.")
            else:
                try:
                    distancia, ruta = dijkstra(CIUDAD, origen, destino)
                    
                    if distancia == float('inf'):
                        print(f"\nNo existe una ruta posible entre {origen} y {destino}.")
                    else:
                        print(f"\nResultado para la ruta: {origen} -> {destino}")
                        print(f"Distancia Total: {distancia}")
                        print(f"Camino Óptimo  : {' -> '.join(ruta)}")
                except ValueError as e:
                    print(f"\n[!] Error del algoritmo: {e}")
                    
        elif opcion == '2':
            print("\n--- MAPA DE LA CIUDAD ---")
            for nodo, conexiones in CIUDAD.items():
                conexiones_str = ", ".join([f"{v} ({p} min)" for v, p in conexiones.items()])
                print(f"{nodo.ljust(15)} : {conexiones_str}")
                
        elif opcion == '0':
            print("\nSaliendo...")
            break
        else:
            print("\n[!] Opción no válida.")
