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

def imprimir_resultado_coloreo(grafo: Grafo, asignacion: Dict[str, int]):
    """Imprime de forma clara la asignación de franjas horarias y verifica si no hay choques."""
    es_valido = verificar_coloreo(grafo, asignacion)
    
    franjas: Dict[int, List[str]] = {}
    for nodo, color in asignacion.items():
        if color not in franjas:
            franjas[color] = []
        franjas[color].append(nodo)
        
    print(f"\nSe utilizaron {len(franjas)} franjas horarias (colores).")
    print(f"¿La asignación es válida (sin choques)? {'Sí' if es_valido else 'No'}\n")
    
    for color in sorted(franjas.keys()):
        print(f"Franja {color + 1}:")
        for nodo in franjas[color]:
            print(f"  - {nodo}")

if __name__ == "__main__":
    while True:
        print("\n=== COLOREO DE GRAFOS (ORGANIZACIÓN DE EXÁMENES) ===")
        print("1. Ver demostración con el mapa de materias por defecto (11 vértices)")
        print("2. Crear e ingresar un grafo de conflictos personalizado")
        print("0. Salir")
        
        opcion = input("\nElige una opción (0-2): ").strip()
        
        if opcion == '1':
            print("\n--- GRAFO DE MATERIAS POR DEFECTO ---")
            asignacion = coloreo_voraz(MATERIAS_CONFLICTO)
            imprimir_resultado_coloreo(MATERIAS_CONFLICTO, asignacion)
            
        elif opcion == '2':
            print("\n--- CREACIÓN DE GRAFO PERSONALIZADO ---")
            try:
                n = int(input("¿Cuántas materias/nodos deseas ingresar?: "))
                if n <= 0:
                    print("[!] Debes ingresar al menos 1 materia.")
                    continue
                    
                grafo_personalizado: Grafo = {}
                materias = []
                print(f"Ingresa los nombres de las {n} materias:")
                for i in range(n):
                    mat = input(f"Materia {i+1}: ").strip()
                    while not mat or mat in grafo_personalizado:
                        mat = input(f"Nombre inválido o duplicado. Materia {i+1}: ").strip()
                    grafo_personalizado[mat] = set()
                    materias.append(mat)
                    
                print("\nAhora ingresa los conflictos (estudiantes inscritos en ambas).")
                print("Escribe los nombres de los dos nodos separados por coma (ej. Mat1, Mat2).")
                print("Escribe 'fin' para terminar de ingresar conflictos.")
                
                while True:
                    linea = input("Conflicto (o 'fin'): ").strip()
                    if linea.lower() == 'fin':
                        break
                    partes = [p.strip() for p in linea.split(',')]
                    if len(partes) == 2 and partes[0] in grafo_personalizado and partes[1] in grafo_personalizado:
                        u, v = partes[0], partes[1]
                        if u != v:
                            grafo_personalizado[u].add(v)
                            grafo_personalizado[v].add(u)
                            print(f"  [+] Conflicto registrado entre '{u}' y '{v}'")
                        else:
                            print("  [!] Una materia no puede estar en conflicto consigo misma.")
                    else:
                        print("  [!] Formato inválido o las materias no existen en la lista.")
                        
                print("\nCalculando coloreo voraz para el grafo ingresado...")
                asignacion = coloreo_voraz(grafo_personalizado)
                imprimir_resultado_coloreo(grafo_personalizado, asignacion)
                
            except ValueError:
                print("\n[!] Error: Debes ingresar un número entero válido.")
                
        elif opcion == '0':
            print("\nSaliendo del programa...")
            break
        else:
            print("\n[!] Opción no válida.")

