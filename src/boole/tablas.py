"""
Ejercicio 7.
Permite evaluar expresiones booleanas y generar sus tablas de verdad 
completas para 3 o 4 variables lógicas (A, B, C, D).
"""

import itertools
from typing import Callable, List, Tuple

# --- Expresiones Booleanas Definidas ---

def expresion_1(A: bool, B: bool, C: bool, D: bool = False) -> bool:
    """(A ∧ B) ∨ (¬C)"""
    return (A and B) or (not C)

def expresion_2(A: bool, B: bool, C: bool, D: bool = False) -> bool:
    """(A ⊕ B) ∧ C"""
    # En Python, el XOR booleano se puede representar con el operador ^ 
    # o como A != B
    return (A ^ B) and C

def expresion_3(A: bool, B: bool, C: bool, D: bool = False) -> bool:
    """(A ∨ B) ∧ (¬A ∨ C)"""
    return (A or B) and ((not A) or C)

def expresion_personalizada(A: bool, B: bool, C: bool, D: bool) -> bool:
    """Ejemplo de expresión usando 4 variables: (A ∧ B) ∨ (C ⊕ D)"""
    return (A and B) or (C ^ D)


# --- Lógica de Generación ---

def evaluar_entrada_concreta(func: Callable, A: bool, B: bool, C: bool, D: bool = False) -> bool:
    """Evalúa la función booleana para una combinación específica de entradas."""
    return func(A, B, C, D)

def generar_tabla_verdad(nombre: str, func: Callable, num_vars: int = 3) -> List[Tuple[Tuple[bool, ...], bool]]:
    """
    Genera e imprime la tabla de verdad para una función booleana.
    Retorna una lista con las filas: (combinación_tupla, resultado).
    """
    nombres_vars = ["A", "B", "C", "D"][:num_vars]
    combinaciones = list(itertools.product([False, True], repeat=num_vars))
    
    # Formateo visual
    encabezado = " | ".join(nombres_vars) + " || Resultado"
    separador = "-" * len(encabezado)
    
    print(f"\n--- Tabla de verdad: {nombre} ---")
    print(separador)
    print(encabezado)
    print(separador)
    
    resultados_tabla = []
    
    for comb in combinaciones:
        # Extraer variables con desempaquetado y evaluar (rellenando D si es necesario)
        if num_vars == 3:
            res = func(comb[0], comb[1], comb[2], False)
        elif num_vars == 4:
            res = func(comb[0], comb[1], comb[2], comb[3])
        else:
            raise ValueError("Solo se soportan 3 o 4 variables.")
            
        # Convertir a 0s y 1s para impresión
        fila_str = " | ".join(["1" if val else "0" for val in comb])
        res_str = "1" if res else "0"
        
        print(f"{fila_str} ||    {res_str}")
        resultados_tabla.append((comb, res))
        
    print(separador)
    return resultados_tabla


if __name__ == "__main__":
    opciones_expresiones = {
        '1': ("(A ∧ B) ∨ (¬C)", expresion_1, 3),
        '2': ("(A ⊕ B) ∧ C", expresion_2, 3),
        '3': ("(A ∨ B) ∧ (¬A ∨ C)", expresion_3, 3),
        '4': ("(A ∧ B) ∨ (C ⊕ D)", expresion_personalizada, 4)
    }

    while True:
        print("\n=== TABLAS DE VERDAD Y CIRCUITOS LÓGICOS ===")
        print("1. Generar tabla de (A ∧ B) ∨ (¬C)")
        print("2. Generar tabla de (A ⊕ B) ∧ C")
        print("3. Generar tabla de (A ∨ B) ∧ (¬A ∨ C)")
        print("4. Generar tabla de (A ∧ B) ∨ (C ⊕ D)  [4 Variables]")
        print("5. Evaluar entrada concreta manualmente")
        print("0. Salir")
        
        try:
            opcion = input("\nElige una opción (0-5): ").strip()
            
            if opcion in ['1', '2', '3', '4']:
                nombre, func, num_vars = opciones_expresiones[opcion]
                generar_tabla_verdad(nombre, func, num_vars)
                
            elif opcion == '5':
                print("\nSelecciona la expresión a evaluar:")
                for k, v in opciones_expresiones.items():
                    print(f"{k}. {v[0]}")
                
                sub_opc = input("Elige (1-4): ").strip()
                if sub_opc in opciones_expresiones:
                    nombre, func, num_vars = opciones_expresiones[sub_opc]
                    print("\nIngresa los valores (1 para Verdadero, 0 para Falso):")
                    
                    val_A = input("Valor de A: ").strip() == '1'
                    val_B = input("Valor de B: ").strip() == '1'
                    val_C = input("Valor de C: ").strip() == '1'
                    
                    if num_vars == 4:
                        val_D = input("Valor de D: ").strip() == '1'
                    else:
                        val_D = False
                        
                    resultado = evaluar_entrada_concreta(func, val_A, val_B, val_C, val_D)
                    res_str = "1 (Verdadero)" if resultado else "0 (Falso)"
                    
                    print(f"\nAl evaluar {nombre} con la entrada dada:")
                    print(f"Resultado final: {res_str}")
                else:
                    print("\n[!] Expresión no válida.")
                    
            elif opcion == '0':
                print("\nSaliendo del programa...")
                break
                
            else:
                print("\n[!] Opción no válida. Inténtalo de nuevo.")
                
        except KeyboardInterrupt:
            print("\n[!] Operación cancelada por el usuario. Saliendo...")
            break
