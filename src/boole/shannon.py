"""
Módulo para el cálculo de Entropía de Shannon (Ejercicio 9).

Calcula frecuencias, probabilidades y entropía de Shannon de textos.
Permite comparar la entropía entre diferentes mensajes.
"""

import math
from collections import Counter
from typing import Dict, Tuple

def calcular_frecuencias(texto: str) -> Dict[str, int]:
    """Calcula la frecuencia absoluta de cada símbolo en el texto."""
    if not texto:
        return {}
    return dict(Counter(texto))

def calcular_probabilidades(texto: str) -> Dict[str, float]:
    """Calcula la probabilidad (frecuencia relativa) de cada símbolo."""
    if not texto:
        return {}
    frecuencias = calcular_frecuencias(texto)
    total = len(texto)
    return {simbolo: frec / total for simbolo, frec in frecuencias.items()}

def calcular_entropia(texto: str) -> float:
    """
    Calcula la entropía de Shannon H = -sum(p_i * log2(p_i)).
    Retorna 0.0 si el texto está vacío.
    """
    if not texto:
        return 0.0
    probabilidades = calcular_probabilidades(texto)
    entropia = -sum(p * math.log2(p) for p in probabilidades.values() if p > 0)
    return entropia

def comparar_textos(texto1: str, texto2: str) -> Tuple[float, float, str]:
    """
    Compara la entropía de dos textos y devuelve un análisis.
    Retorna (entropia1, entropia2, explicacion).
    """
    h1 = calcular_entropia(texto1)
    h2 = calcular_entropia(texto2)
    
    if h1 > h2:
        mayor = "El Texto 1"
        razon = "tiene una mayor variedad de símbolos y una distribución más uniforme"
    elif h2 > h1:
        mayor = "El Texto 2"
        razon = "tiene una mayor variedad de símbolos y una distribución más uniforme"
    else:
        return h1, h2, "Ambos textos tienen exactamente la misma entropía (misma incertidumbre por símbolo)."
        
    explicacion = f"{mayor} tiene mayor entropía ({max(h1, h2):.4f} bits/símbolo). Esto ocurre porque {razon}, lo que genera mayor incertidumbre al adivinar el siguiente carácter, a diferencia del otro texto que es más predecible o repetitivo."
    return h1, h2, explicacion

if __name__ == "__main__":
    while True:
        print("\n=== ENTROPÍA DE SHANNON ===")
        print("1. Calcular frecuencias, probabilidades y entropía de un texto")
        print("2. Comparar la entropía de dos textos")
        print("3. Ver demostración por defecto (texto repetitivo vs variado)")
        print("0. Salir")
        
        try:
            opcion = input("\nElige una opción (0-3): ").strip()
            
            if opcion == '1':
                texto = input("Ingresa el texto a analizar: ")
                if not texto:
                    print("\n[!] El texto está vacío.")
                    continue
                    
                print(f"\nLongitud del texto: {len(texto)} caracteres")
                probabilidades = calcular_probabilidades(texto)
                print("\nSímbolo | Probabilidad")
                print("-" * 22)
                for sim, p in sorted(probabilidades.items(), key=lambda item: item[1], reverse=True):
                    repr_sim = repr(sim) if sim.isspace() else sim
                    print(f"{repr_sim:7} | {p:.4f}")
                    
                entropia = calcular_entropia(texto)
                print("-" * 22)
                print(f"Entropía Total (H): {entropia:.4f} bits/símbolo")
                
            elif opcion == '2':
                t1 = input("Ingresa el primer texto: ")
                t2 = input("Ingresa el segundo texto: ")
                
                if not t1 or not t2:
                    print("\n[!] Ninguno de los textos puede estar vacío.")
                    continue
                    
                h1, h2, explicacion = comparar_textos(t1, t2)
                print(f"\nEntropía Texto 1: {h1:.4f} bits")
                print(f"Entropía Texto 2: {h2:.4f} bits")
                print(f"\nAnálisis: {explicacion}")
                
            elif opcion == '3':
                t_repetitivo = "AAAAAAAAAAAAAAAABBB"
                t_variado = "MURCIELAGO 123456789"
                
                print("\n[Demostración]")
                print(f"Texto Repetitivo: '{t_repetitivo}'")
                print(f"Texto Variado   : '{t_variado}'")
                
                h1, h2, explicacion = comparar_textos(t_repetitivo, t_variado)
                print(f"\nEntropía del texto repetitivo : {h1:.4f} bits/símbolo")
                print(f"Entropía del texto variado    : {h2:.4f} bits/símbolo")
                print(f"\nConclusión: {explicacion}")
                
            elif opcion == '0':
                print("\nSaliendo del programa...")
                break
            else:
                print("\n[!] Opción no válida. Inténtalo de nuevo.")
                
        except KeyboardInterrupt:
            print("\n[!] Operación cancelada por el usuario. Saliendo...")
            break
