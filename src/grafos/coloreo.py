"""
Coloreo de Grafos usando algoritmo Voraz (Greedy).
Ejercicio 6 del Taller 3.
Permite organizar exámenes sin choques para estudiantes en cursos conflictivos.
"""

from typing import Dict, List, Set

# Definición del tipo Grafo: Diccionario donde cada clave es un nodo y el valor es una lista o set de vecinos
Grafo = Dict[str, Set[str]]

def coloreo_voraz(grafo: Grafo) -> Dict[str, int]:
    """
    Asigna colores a los vértices de un grafo usando un algoritmo voraz.
    Trata de ordenar los nodos por grado (Welsh-Powell) para obtener un mejor resultado.
    
    Parámetros:
        grafo (Grafo): Grafo representado como lista de adyacencia.
        
    Retorna:
        Dict[str, int]: Un diccionario mapeando cada vértice a un número de color (0, 1, 2...).
    """
    # Ordenar los vértices por grado de mayor a menor (heurística de Welsh-Powell)
    # Esto ayuda a que el algoritmo voraz use menos colores en general.
    vertices_ordenados = sorted(grafo.keys(), key=lambda v: len(grafo[v]), reverse=True)
    
    asignacion = {}
    
    for vertice in vertices_ordenados:
        # Encontrar colores usados por los vecinos ya coloreados
        colores_vecinos = set()
        for vecino in grafo[vertice]:
            if vecino in asignacion:
                colores_vecinos.add(asignacion[vecino])
                
        # Encontrar el color (entero >= 0) más pequeño disponible
        color = 0
        while color in colores_vecinos:
            color += 1
            
        asignacion[vertice] = color
        
    return asignacion

def verificar_coloreo(grafo: Grafo, asignacion: Dict[str, int]) -> bool:
    """
    Verifica que no haya dos vértices adyacentes con el mismo color.
    
    Parámetros:
        grafo (Grafo): El grafo original.
        asignacion (Dict[str, int]): El diccionario con los colores asignados.
        
    Retorna:
        bool: True si la asignación es válida, False en caso contrario.
    """
    for vertice, vecinos in grafo.items():
        if vertice not in asignacion:
            return False
        color_actual = asignacion[vertice]
        for vecino in vecinos:
            if vecino in asignacion and asignacion[vecino] == color_actual:
                return False
    return True

# Grafo de prueba: Conflictos de horarios de exámenes (10 vértices)
# Vértices: Cursos
# Aristas: Si dos cursos están conectados, hay estudiantes en ambos (no pueden ser a la misma hora)
MATERIAS_CONFLICTO: Grafo = {
    "Cálculo": {"Física", "Programación", "Álgebra"},
    "Física": {"Cálculo", "Química", "Biología"},
    "Programación": {"Cálculo", "Discretas", "BasesDatos"},
    "Discretas": {"Programación", "Álgebra", "Lógica"},
    "Álgebra": {"Cálculo", "Discretas", "Lógica"},
    "Química": {"Física", "Biología"},
    "Biología": {"Física", "Química", "Estadística"},
    "BasesDatos": {"Programación", "Redes"},
    "Redes": {"BasesDatos", "Estadística"},
    "Lógica": {"Discretas", "Álgebra"},
    "Estadística": {"Biología", "Redes"}
}

if __name__ == "__main__":
    print("\n=== COLOREO DE GRAFOS (ORGANIZACIÓN DE EXÁMENES) ===")
    
    print("\nCalculando asignación de franjas horarias...")
    asignacion = coloreo_voraz(MATERIAS_CONFLICTO)
    
    es_valido = verificar_coloreo(MATERIAS_CONFLICTO, asignacion)
    
    # Agrupar por colores para mostrar los resultados de forma amigable
    franjas: Dict[int, List[str]] = {}
    for materia, color in asignacion.items():
        if color not in franjas:
            franjas[color] = []
        franjas[color].append(materia)
        
    print(f"\nSe utilizaron {len(franjas)} franjas horarias (colores).")
    print(f"¿La asignación es válida (sin choques)? {'Sí' if es_valido else 'No'}\n")
    
    for color in sorted(franjas.keys()):
        print(f"Franja {color + 1}:")
        for materia in franjas[color]:
            print(f"  - {materia}")
            
    print("\nDemostración finalizada.")
