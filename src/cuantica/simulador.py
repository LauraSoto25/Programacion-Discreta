"""
Simulador Cuántico Básico.
Ejercicio 10 del Taller 3.
Permite simular el comportamiento de un qubit aplicando compuertas X, Z y H, 
y extraer probabilidades simulando 1000 mediciones.
"""

import math
import random
from typing import List, Tuple

# Un estado cuántico de un qubit se representa como [alpha, beta]
# donde alpha y beta pueden ser números complejos.
EstadoQubit = List[complex]
Matriz2x2 = List[List[complex]]

# Definición de las compuertas (puertas) cuánticas básicas
COMPUERTA_X: Matriz2x2 = [
    [0, 1],
    [1, 0]
]

COMPUERTA_Z: Matriz2x2 = [
    [1, 0],
    [0, -1]
]

# 1 / sqrt(2)
INV_SQRT2 = 1.0 / math.sqrt(2)

COMPUERTA_H: Matriz2x2 = [
    [INV_SQRT2, INV_SQRT2],
    [INV_SQRT2, -INV_SQRT2]
]

def crear_qubit(estado_base: int) -> EstadoQubit:
    """Crea un qubit en estado |0> o |1>."""
    if estado_base == 0:
        return [1 + 0j, 0 + 0j]  # |0>
    elif estado_base == 1:
        return [0 + 0j, 1 + 0j]  # |1>
    else:
        raise ValueError("El estado base debe ser 0 o 1")

def aplicar_compuerta(compuerta: Matriz2x2, estado: EstadoQubit) -> EstadoQubit:
    """
    Multiplica la matriz de la compuerta 2x2 por el vector estado 2x1.
    Retorna el nuevo vector estado.
    """
    nuevo_estado = [0j, 0j]
    nuevo_estado[0] = compuerta[0][0] * estado[0] + compuerta[0][1] * estado[1]
    nuevo_estado[1] = compuerta[1][0] * estado[0] + compuerta[1][1] * estado[1]
    return nuevo_estado

def calcular_probabilidades(estado: EstadoQubit) -> Tuple[float, float]:
    """
    Calcula las probabilidades de colapsar en |0> o |1>.
    Probabilidad = |amplitud|^2
    """
    prob_0 = abs(estado[0])**2
    prob_1 = abs(estado[1])**2
    return prob_0, prob_1

def formatear_estado(estado: EstadoQubit) -> str:
    """Formatea el vector estado de manera legible para el humano."""
    # Redondeo para evitar cosas como 0.0000000000000001
    def formatear_complejo(c):
        real = round(c.real, 4)
        imag = round(c.imag, 4)
        if imag == 0:
            return f"{real}"
        elif real == 0:
            return f"{imag}i"
        else:
            return f"{real}{'+' if imag > 0 else ''}{imag}i"

    alpha_str = formatear_complejo(estado[0])
    beta_str = formatear_complejo(estado[1])
    return f"[{alpha_str}]|0> + [{beta_str}]|1>"

def simular_mediciones(estado: EstadoQubit, num_mediciones: int = 1000) -> Tuple[int, int]:
    """
    Simula múltiples colapsos de la función de onda basado en las probabilidades.
    Retorna la cantidad de veces que se midió 0 y la cantidad de veces que se midió 1.
    """
    prob_0, prob_1 = calcular_probabilidades(estado)
    conteo_0 = 0
    conteo_1 = 0
    
    for _ in range(num_mediciones):
        # random.random() devuelve un float entre 0.0 y 1.0
        if random.random() < prob_0:
            conteo_0 += 1
        else:
            conteo_1 += 1
            
    return conteo_0, conteo_1

def mostrar_analisis(estado: EstadoQubit, num_mediciones: int = 1000):
    """Muestra el estado matemático y la simulación empírica de probabilidades."""
    print(f"Estado matemático: {formatear_estado(estado)}")
    prob_0, prob_1 = calcular_probabilidades(estado)
    print(f"Probabilidades Teóricas -> |0>: {prob_0*100:.2f}% | |1>: {prob_1*100:.2f}%")
    
    c_0, c_1 = simular_mediciones(estado, num_mediciones)
    print(f"Resultados (1000 mediciones) -> Medido '0': {c_0} veces | Medido '1': {c_1} veces")
    print(f"Frecuencias Empíricas -> |0>: {(c_0/num_mediciones)*100:.2f}% | |1>: {(c_1/num_mediciones)*100:.2f}%\n")

if __name__ == "__main__":
    while True:
        print("\n=== SIMULADOR CUÁNTICO BÁSICO (1 QUBIT) ===")
        print("1. Ejecutar casos de prueba obligatorios (X, H, HH)")
        print("2. Modo Interactivo: Crea tu propio circuito")
        print("0. Salir")
        
        opcion = input("\nElige una opción (0-2): ").strip()
        
        if opcion == '1':
            print("\n--- CASOS OBLIGATORIOS ---")
            
            # Caso 1: X|0> = |1>
            print("1. Compuerta X sobre |0> (NOT cuántico)")
            q1 = crear_qubit(0)
            q1 = aplicar_compuerta(COMPUERTA_X, q1)
            mostrar_analisis(q1)
            
            # Caso 2: H|0> produce 50% y 50%
            print("2. Compuerta Hadamard (H) sobre |0> (Superposición)")
            q2 = crear_qubit(0)
            q2 = aplicar_compuerta(COMPUERTA_H, q2)
            mostrar_analisis(q2)
            
            # Caso 3: HH|0> = |0>
            print("3. Compuerta Hadamard doble (HH) sobre |0> (Reversibilidad)")
            q3 = crear_qubit(0)
            q3 = aplicar_compuerta(COMPUERTA_H, q3)
            q3 = aplicar_compuerta(COMPUERTA_H, q3)
            mostrar_analisis(q3)
            
        elif opcion == '2':
            print("\n--- MODO INTERACTIVO ---")
            try:
                base = int(input("¿Con qué estado base deseas iniciar? (0 o 1): "))
                if base not in [0, 1]:
                    print("[!] Por favor ingresa 0 o 1.")
                    continue
                
                estado_actual = crear_qubit(base)
                print(f"\nEstado inicial: {formatear_estado(estado_actual)}")
                
                mapa_compuertas = {'X': COMPUERTA_X, 'Z': COMPUERTA_Z, 'H': COMPUERTA_H}
                print("\nCompuertas disponibles: X (NOT), Z (Phase Flip), H (Hadamard)")
                
                secuencia = input("Ingresa la secuencia de compuertas (ej. H X Z) o presiona Enter para ninguna: ").strip().upper()
                
                if secuencia:
                    puertas = secuencia.split()
                    for p in puertas:
                        if p in mapa_compuertas:
                            print(f"Aplicando compuerta {p}...")
                            estado_actual = aplicar_compuerta(mapa_compuertas[p], estado_actual)
                        else:
                            print(f"[!] Ignorando compuerta desconocida: {p}")
                
                print("\n--- RESULTADO FINAL ---")
                mostrar_analisis(estado_actual)
                
            except ValueError:
                print("\n[!] Error: Entrada no válida.")
                
        elif opcion == '0':
            print("\nSaliendo del simulador...")
            break
        else:
            print("\n[!] Opción no válida.")
