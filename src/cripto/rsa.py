"""
Simulador de RSA de Juguete.
Permite generar llaves, cifrar y descifrar usando aritmética modular.
Incluye implementación manual del Algoritmo de Euclides Extendido.
"""

from typing import Tuple

def euclides_extendido(a: int, b: int) -> Tuple[int, int, int]:
    """
    Algoritmo de Euclides Extendido.
    Calcula el máximo común divisor (gcd) de 'a' y 'b', y los coeficientes 'x' e 'y'
    tales que: a * x + b * y = gcd(a, b).
    
    Parámetros:
        a (int): Primer número entero.
        b (int): Segundo número entero.
        
    Retorna:
        Tuple[int, int, int]: Una tupla con (gcd, x, y).
    """
    if a == 0:
        return b, 0, 1
        
    gcd, x1, y1 = euclides_extendido(b % a, a)
    
    # Actualizar x y y usando los resultados de la llamada recursiva
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd, x, y

def inverso_modular(e: int, phi: int) -> int:
    """
    Calcula el inverso modular de 'e' módulo 'phi'.
    
    Parámetros:
        e (int): Exponente público.
        phi (int): Valor de la función indicatriz de Euler, phi(n).
        
    Retorna:
        int: El inverso modular 'd' de 'e' módulo 'phi', de modo que (e * d) % phi == 1.
        
    Excepciones:
        ValueError: Si el inverso modular no existe (es decir, gcd(e, phi) != 1).
    """
    gcd, x, y = euclides_extendido(e, phi)
    
    if gcd != 1:
        raise ValueError(f"El exponente e={e} no es coprimo con phi={phi} (MCD={gcd}). No tiene inverso modular.")
        
    # Asegurar que el inverso sea positivo
    return x % phi

def generar_llaves(p: int, q: int, e: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Genera las llaves pública y privada de RSA.
    
    Parámetros:
        p (int): Primer número primo.
        q (int): Segundo número primo.
        e (int): Exponente público elegido.
        
    Retorna:
        Tuple[Tuple[int, int], Tuple[int, int]]: ((e, n), (d, n)), donde la primera tupla
        es la llave pública y la segunda la llave privada.
    """
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Esto lanzará ValueError si e no es válido
    d = inverso_modular(e, phi)
    
    return (e, n), (d, n)

def cifrar(M: int, e: int, n: int) -> int:
    """
    Cifra un mensaje numérico M utilizando la llave pública (e, n).
    
    Parámetros:
        M (int): Mensaje en texto claro numérico (M < n).
        e (int): Exponente público.
        n (int): Módulo público.
        
    Retorna:
        int: Mensaje cifrado C.
    """
    if M >= n:
        raise ValueError("El mensaje M debe ser estrictamente menor que n.")
    return pow(M, e, n)

def descifrar(C: int, d: int, n: int) -> int:
    """
    Descifra un mensaje cifrado C utilizando la llave privada (d, n).
    
    Parámetros:
        C (int): Mensaje cifrado.
        d (int): Exponente privado.
        n (int): Módulo público.
        
    Retorna:
        int: Mensaje original numérico M.
    """
    return pow(C, d, n)


if __name__ == "__main__":
    while True:
        print("\n=== RSA DE JUGUETE ===")
        print("1. Cifrar un mensaje manual")
        print("2. Descifrar un mensaje manual")
        print("3. Ver caso de prueba obligatorio")
        print("0. Salir")
        
        try:
            opcion = input("\nElige una opción (0-3): ").strip()
            
            if opcion == '1':
                p = int(input("Ingresa el primer primo p: "))
                q = int(input("Ingresa el segundo primo q: "))
                n = p * q
                phi = (p - 1) * (q - 1)
                
                print(f"-> Calculado: n = {n}, phi(n) = {phi}")
                
                # Bucle para asegurar un e válido
                while True:
                    e = int(input("Ingresa el exponente público e: "))
                    try:
                        d = inverso_modular(e, phi)
                        break
                    except ValueError as err:
                        print(f"[!] Error: {err}. Intenta con otro valor.")
                
                print(f"-> Calculado: exponente privado d = {d}")
                print(f"-> Llave pública: ({e}, {n})")
                print(f"-> Llave privada: ({d}, {n})")
                
                M = int(input(f"Ingresa el mensaje M a cifrar (entero menor a {n}): "))
                if M >= n:
                    print("[!] Error: El mensaje es más grande que n, no se puede cifrar correctamente.")
                else:
                    C = cifrar(M, e, n)
                    print(f"\nResultado Cifrado (C): {C}")
                
            elif opcion == '2':
                C = int(input("Ingresa el mensaje cifrado C: "))
                d = int(input("Ingresa el exponente privado d: "))
                n = int(input("Ingresa el módulo n: "))
                
                M_descifrado = descifrar(C, d, n)
                print(f"\nResultado Descifrado (M): {M_descifrado}")
                
            elif opcion == '3':
                p = 61
                q = 53
                e = 17
                M = 65
                
                print(f"\nDatos iniciales: p={p}, q={q}, e={e}, Mensaje M={M}")
                n = p * q
                phi = (p - 1) * (q - 1)
                d = inverso_modular(e, phi)
                
                C = cifrar(M, e, n)
                M_descifrado = descifrar(C, d, n)
                
                print(f"n = {n}")
                print(f"phi(n) = {phi}")
                print(f"Inverso modular (d) = {d}")
                print(f"Mensaje Cifrado (C) = {C}")
                print(f"Mensaje Descifrado (M) = {M_descifrado}")
                if M == M_descifrado:
                    print("¡Éxito! El mensaje descifrado coincide con el original.")
                else:
                    print("[!] Algo salió mal.")
                    
            elif opcion == '0':
                print("\nSaliendo del simulador RSA...")
                break
            else:
                print("\n[!] Opción no válida. Inténtalo de nuevo.")
                
        except ValueError:
            print("\n[!] Error: Se esperaba un valor numérico entero.")
        except KeyboardInterrupt:
            print("\n[!] Operación cancelada por el usuario. Saliendo...")
            break
