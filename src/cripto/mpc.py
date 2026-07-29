"""
Simula un protocolo de suma secreta con tres servidores para calcular
un promedio de notas sin que ningún servidor conozca los datos individuales,
usando aritmética modular.
"""

import random
from typing import List, Tuple

# Módulo M suficientemente grande
M_DEFAULT = 1000003

class ServidorMPC:
    def __init__(self, id_servidor: int):
        self.id_servidor = id_servidor
        self.fragmentos = []

    def recibir_fragmento(self, fragmento: int):
        self.fragmentos.append(fragmento)

    def calcular_suma_parcial(self, M: int) -> int:
        return sum(self.fragmentos) % M

    def resetear(self):
        self.fragmentos = []


def dividir_nota(nota: int, M: int) -> Tuple[int, int, int]:
    """
    Divide una nota en tres fragmentos aleatorios tales que
    (s1 + s2 + s3) % M == nota % M.
    """
    s1 = random.randint(0, M - 1)
    s2 = random.randint(0, M - 1)
    # nota = (s1 + s2 + s3) mod M  =>  s3 = (nota - s1 - s2) mod M
    s3 = (nota - s1 - s2) % M
    return (s1, s2, s3)


def simular_mpc(notas: List[int], M: int = M_DEFAULT) -> Tuple[int, float, List[int]]:
    """
    Ejecuta el protocolo MPC con 3 servidores.
    
    Retorna:
        - La suma total reconstruida
        - El promedio
        - Las sumas parciales de cada servidor (para poder ver qué calcularon)
    """
    if not notas:
        return 0, 0.0, [0, 0, 0]
        
    # Validar que la suma total no exceda M, de lo contrario la reconstrucción fallará
    suma_real = sum(notas)
    if suma_real >= M:
        raise ValueError(f"La suma de las notas ({suma_real}) excede el módulo M ({M}). El protocolo fallará.")

    servidores = [ServidorMPC(1), ServidorMPC(2), ServidorMPC(3)]
    
    # Fase 1: Dividir y distribuir los secretos
    for nota in notas:
        s1, s2, s3 = dividir_nota(nota, M)
        servidores[0].recibir_fragmento(s1)
        servidores[1].recibir_fragmento(s2)
        servidores[2].recibir_fragmento(s3)
        
    # Fase 2: Cada servidor calcula su suma parcial (computación local)
    sumas_parciales = [s.calcular_suma_parcial(M) for s in servidores]
    
    # Fase 3: Reconstrucción pública de la suma y el promedio
    suma_total_reconstruida = sum(sumas_parciales) % M
    promedio = suma_total_reconstruida / len(notas)
    
    return suma_total_reconstruida, promedio, sumas_parciales


if __name__ == "__main__":
    while True:
        print("\n=== MPC BÁSICO (Promedio Seguro) ===")
        print("1. Ingresar notas manualmente y calcular promedio")
        print("2. Ver demostración por defecto (notas: 40, 35, 50, 25)")
        print("0. Salir")
        
        try:
            opcion = input("\nElige una opción (0-2): ").strip()
            
            if opcion == '1':
                entrada = input("Ingresa las notas separadas por espacios (ej: 40 35 50 25): ")
                notas = []
                for x in entrada.split():
                    nota = int(x)
                    if not 0 <= nota <= 50:
                        print(f"[!] Advertencia: La nota {nota} no está en el rango esperado (0-50).")
                    notas.append(nota)
                
                if not notas:
                    print("\nNo ingresaste ninguna nota.")
                    continue
                    
                print(f"\nNotas a procesar: {len(notas)}")
                print(f"Módulo utilizado (M): {M_DEFAULT}")
                
                suma, prom, parciales = simular_mpc(notas, M_DEFAULT)
                
                print("\n=== FASE DE SERVIDORES ===")
                for i, p in enumerate(parciales):
                    print(f"Servidor {i+1} reporta suma parcial: {p}")
                    
                print("\n=== RECONSTRUCCIÓN FINAL ===")
                print(f"Suma total reconstruida: {suma}")
                print(f"Promedio: {prom}")
                
            elif opcion == '2':
                notas = [40, 35, 50, 25]
                print("\n[Demostración]")
                print(f"Notas secretas de los estudiantes: {notas}")
                
                suma, prom, parciales = simular_mpc(notas, M_DEFAULT)
                
                print("\n=== FASE DE SERVIDORES ===")
                for i, p in enumerate(parciales):
                    print(f"Servidor {i+1} reporta suma parcial: {p}")
                
                print("\n=== RECONSTRUCCIÓN FINAL ===")
                print(f"Suma total reconstruida: {suma}")
                print(f"Promedio: {prom}")
                print("\nResultado esperado: Suma = 150, Promedio = 37.5")
                
            elif opcion == '0':
                print("\nSaliendo del programa...")
                break
            else:
                print("\n[!] Opción no válida. Inténtalo de nuevo.")
                
        except ValueError as e:
            if "excede el módulo" in str(e):
                print(f"\n[!] Error: {e}")
            else:
                print("\n[!] Error: Por favor, asegúrate de ingresar solo números enteros.")
        except KeyboardInterrupt:
            print("\n[!] Operación cancelada por el usuario. Saliendo...")
            break
