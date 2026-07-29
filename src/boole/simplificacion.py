"""
Simplificación Booleana usando el algoritmo tabular de Quine-McCluskey.
Ejercicio 8 del Taller 3.
"""

from typing import List, Set, Dict, Tuple

def int_a_binario_str(num: int, num_vars: int) -> str:
    """Convierte un entero a su representación binaria en string con ceros a la izquierda."""
    return format(num, f'0{num_vars}b')

def difieren_en_un_bit(term1: str, term2: str) -> int:
    """
    Compara dos términos binarios/guiones. Si difieren en exactamente 1 posición, 
    retorna el índice de la diferencia. Si no, retorna -1.
    """
    diferencias = 0
    indice = -1
    for i in range(len(term1)):
        if term1[i] != term2[i]:
            diferencias += 1
            indice = i
            if diferencias > 1:
                return -1
    return indice if diferencias == 1 else -1

def agrupar_terminos(terminos: Set[str]) -> Tuple[Set[str], Set[str]]:
    """
    Realiza una pasada de simplificación encontrando pares que difieren en un bit.
    Retorna (nuevos_terminos_agrupados, terminos_no_agrupados).
    """
    marcados = set()
    nuevos_terminos = set()
    terminos_lista = list(terminos)
    
    for i in range(len(terminos_lista)):
        for j in range(i + 1, len(terminos_lista)):
            idx = difieren_en_un_bit(terminos_lista[i], terminos_lista[j])
            if idx != -1:
                marcados.add(terminos_lista[i])
                marcados.add(terminos_lista[j])
                nuevo_term = terminos_lista[i][:idx] + '-' + terminos_lista[i][idx+1:]
                nuevos_terminos.add(nuevo_term)
                
    no_agrupados = set(terminos_lista) - marcados
    return nuevos_terminos, no_agrupados

def obtener_implicantes_primos(minterminos_bin: Set[str]) -> Set[str]:
    """Obtiene todos los implicantes primos aplicando agrupaciones sucesivas."""
    implicantes_primos = set()
    terminos_actuales = minterminos_bin
    
    while terminos_actuales:
        nuevos_terminos, no_agrupados = agrupar_terminos(terminos_actuales)
        implicantes_primos.update(no_agrupados)
        terminos_actuales = nuevos_terminos
        
    return implicantes_primos

def cubre_mintermino(implicante: str, mintermino_bin: str) -> bool:
    """Verifica si un implicante (con guiones) cubre un minitérmino específico."""
    for i in range(len(implicante)):
        if implicante[i] != '-' and implicante[i] != mintermino_bin[i]:
            return False
    return True

def obtener_implicantes_esenciales(implicantes: Set[str], minterminos_bin: Set[str]) -> Set[str]:
    """
    Selecciona los implicantes esenciales usando una aproximación voraz (para simplificar la versión juguete).
    Garantiza cubrir todos los minitérminos.
    """
    esenciales = set()
    minterminos_restantes = set(minterminos_bin)
    implicantes_lista = list(implicantes)
    
    # 1. Encontrar minitérminos cubiertos por un ÚNICO implicante
    for mint in list(minterminos_restantes):
        cubierto_por = [imp for imp in implicantes_lista if cubre_mintermino(imp, mint)]
        if len(cubierto_por) == 1:
            esencial = cubierto_por[0]
            esenciales.add(esencial)
            # Eliminar minitérminos cubiertos por este esencial
            for m in list(minterminos_restantes):
                if cubre_mintermino(esencial, m):
                    minterminos_restantes.discard(m)
                    
    # 2. Cobertura voraz para los minitérminos restantes
    while minterminos_restantes:
        # Buscar el implicante que cubra la mayor cantidad de minitérminos restantes
        mejor_implicante = None
        max_cobertura = 0
        
        for imp in implicantes_lista:
            if imp in esenciales: continue
            cobertura = sum(1 for m in minterminos_restantes if cubre_mintermino(imp, m))
            if cobertura > max_cobertura:
                max_cobertura = cobertura
                mejor_implicante = imp
                
        if mejor_implicante:
            esenciales.add(mejor_implicante)
            for m in list(minterminos_restantes):
                if cubre_mintermino(mejor_implicante, m):
                    minterminos_restantes.discard(m)
        else:
            break
            
    return esenciales

def termino_a_letras(termino: str, num_vars: int) -> str:
    """Convierte un término '01-1' a 'A\'BC\'D'."""
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:num_vars]
    resultado = ""
    for i, char in enumerate(termino):
        if char == '1':
            resultado += letras[i]
        elif char == '0':
            resultado += letras[i] + "'"
    return resultado if resultado else "1"

def simplificar(minterminos: List[int], num_vars: int) -> str:
    """Ejecuta el flujo completo de simplificación."""
    if not minterminos:
        return "0"
        
    if len(minterminos) == 2**num_vars:
        return "1"
        
    minterminos_bin = {int_a_binario_str(m, num_vars) for m in minterminos}
    implicantes_primos = obtener_implicantes_primos(minterminos_bin)
    esenciales = obtener_implicantes_esenciales(implicantes_primos, minterminos_bin)
    
    expresion_letras = [termino_a_letras(imp, num_vars) for imp in esenciales]
    return " + ".join(sorted(expresion_letras))

def generar_tabla_verdad_original(minterminos: List[int], num_vars: int) -> List[int]:
    """Genera la tabla de verdad (lista de 0s y 1s) para los minitérminos dados."""
    tabla = [0] * (2**num_vars)
    for m in minterminos:
        if m < len(tabla):
            tabla[m] = 1
    return tabla

def evaluar_termino(termino: str, estado_bin: str) -> int:
    """Evalúa si un término (ej '01-1') es verdadero para un estado (ej '0101')."""
    for i, char in enumerate(termino):
        if char != '-' and char != estado_bin[i]:
            return 0
    return 1

def evaluar_implicantes(implicantes: Set[str], num_vars: int) -> List[int]:
    """Evalúa un conjunto de implicantes (Suma de Productos) para todos los estados posibles."""
    if not implicantes:
        return [0] * (2**num_vars)
        
    tabla = []
    for i in range(2**num_vars):
        estado_bin = int_a_binario_str(i, num_vars)
        # Es 1 si CUALQUIER implicante es verdadero
        es_verdadero = any(evaluar_termino(imp, estado_bin) for imp in implicantes)
        tabla.append(1 if es_verdadero else 0)
    return tabla

def comprobar_equivalencia(minterminos: List[int], num_vars: int, implicantes_esenciales: Set[str]) -> bool:
    """Comprueba que la función original y la simplificada tienen exactamente la misma tabla de verdad."""
    if len(minterminos) == 2**num_vars:
        tabla_simplificada = [1] * (2**num_vars)
    else:
        tabla_simplificada = evaluar_implicantes(implicantes_esenciales, num_vars)
        
    tabla_original = generar_tabla_verdad_original(minterminos, num_vars)
    
    return tabla_original == tabla_simplificada

if __name__ == "__main__":
    while True:
        print("\n=== SIMPLIFICACIÓN BOOLEANA ===")
        print("1. Simplificar una función manual")
        print("2. Ver caso de prueba obligatorio (3 variables: 1,3,5,7)")
        print("0. Salir")
        
        opcion = input("\nElige una opción (0-2): ").strip()
        
        if opcion == '1':
            try:
                num_vars = int(input("Ingresa el número de variables (ej. 3 o 4): "))
                if num_vars <= 0 or num_vars > 10:
                    print("[!] Por favor ingresa entre 1 y 10 variables.")
                    continue
                    
                minterminos_input = input(f"Ingresa los minitérminos separados por comas (0 a {2**num_vars - 1}): ")
                if not minterminos_input.strip():
                    minterminos = []
                else:
                    minterminos = [int(m.strip()) for m in minterminos_input.split(",")]
                    
                minterminos = [m for m in minterminos if 0 <= m < 2**num_vars]
                
                expresion = simplificar(minterminos, num_vars)
                print(f"\nMinitérminos originales: {sorted(minterminos)}")
                print(f"Expresión simplificada (SOP): {expresion}")
                
                # Verificación interna
                minterminos_bin = {int_a_binario_str(m, num_vars) for m in minterminos}
                primos = obtener_implicantes_primos(minterminos_bin)
                esenciales = obtener_implicantes_esenciales(primos, minterminos_bin)
                son_equivalentes = comprobar_equivalencia(minterminos, num_vars, esenciales)
                
                print(f"¿Tablas de verdad equivalentes?: {'Sí' if son_equivalentes else 'No'}")
                
            except ValueError:
                print("\n[!] Error: Entrada no válida.")
                
        elif opcion == '2':
            num_vars = 3
            minterminos = [1, 3, 5, 7]
            
            print(f"\nDatos iniciales: Variables={num_vars}, Minitérminos={minterminos}")
            expresion = simplificar(minterminos, num_vars)
            
            minterminos_bin = {int_a_binario_str(m, num_vars) for m in minterminos}
            primos = obtener_implicantes_primos(minterminos_bin)
            esenciales = obtener_implicantes_esenciales(primos, minterminos_bin)
            son_equivalentes = comprobar_equivalencia(minterminos, num_vars, esenciales)
            
            print(f"Expresión simplificada (SOP): {expresion}")
            print(f"¿Tablas de verdad equivalentes?: {'Sí' if son_equivalentes else 'No'}")
            
        elif opcion == '0':
            print("\nSaliendo...")
            break
        else:
            print("\n[!] Opción no válida.")
