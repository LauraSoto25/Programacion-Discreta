""""
Permite cifrar, descifrar y realizar un ataque de fuerza bruta sobre un texto
utilizando la aritmética modular sobre el alfabeto latino de 26 letras.
"""

def cifrar(texto: str, k: int) -> str:
    """
    Cifra un texto usando el cifrado César con un desplazamiento k.
    
    Parámetros:
        texto (str): Mensaje a cifrar.
        k (int): Cantidad de posiciones a desplazar.
        
    Retorna:
        str: Texto cifrado.
        
    Propiedades:
        - Mantiene la distinción entre mayúsculas y minúsculas.
        - Conserva intactos espacios, signos de puntuación, números y caracteres especiales.
        - Maneja valores de k negativos y mayores a 26 mediante la propiedad de periodicidad (k mod 26).
    """
    resultado = []
    
    for caracter in texto:
        if 'A' <= caracter <= 'Z':
            # Mayúsculas: índice en el rango 0..25
            indice = ord(caracter) - ord('A')
            nuevo_indice = (indice + k) % 26
            resultado.append(chr(ord('A') + nuevo_indice))
        elif 'a' <= caracter <= 'z':
            # Minúsculas: índice en el rango 0..25
            indice = ord(caracter) - ord('a')
            nuevo_indice = (indice + k) % 26
            resultado.append(chr(ord('a') + nuevo_indice))
        else:
            # Espacios, números, signos de puntuación, etc.
            resultado.append(caracter)
            
    return "".join(resultado)


def descifrar(texto_cifrado: str, k: int) -> str:
    """
    Descifra un texto cifrado con César aplicando el desplazamiento inverso (-k).
    
    Parámetros:
        texto_cifrado (str): Mensaje cifrado.
        k (int): Desplazamiento original usado al cifrar.
        
    Retorna:
        str: Texto original descifrado.
    """
    return cifrar(texto_cifrado, -k)


def fuerza_bruta(texto_cifrado: str) -> dict[int, str]:
    """
    Realiza un ataque de fuerza bruta probando los 25 desplazamientos posibles (1 a 25)
    en el alfabeto latino de 26 letras.
    
    Parámetros:
        texto_cifrado (str): Mensaje cifrado a interceptar.
        
    Retorna:
        dict[int, str]: Diccionario donde cada clave k (1..25) mapea al texto descifrado resultante.
    """
    resultados = {}
    for k in range(1, 26):
        resultados[k] = descifrar(texto_cifrado, k)
    return resultados


if __name__ == "__main__":
    while True:
        print("\n=== CIFRADO CÉSAR ===")
        print("1. Cifrar un mensaje")
        print("2. Descifrar un mensaje (conociendo k)")
        print("3. Ataque de fuerza bruta (sin conocer k)")
        print("4. Ver demostración por defecto (HOLA UNAL)")
        print("0. Salir")
        
        try:
            opcion = input("\nElige una opción (0-4): ").strip()
            
            if opcion == '1':
                texto = input("Ingresa el texto a cifrar: ")
                k = int(input("Ingresa el desplazamiento k (entero): "))
                print("\nResultado Cifrado:", cifrar(texto, k))
                
            elif opcion == '2':
                texto = input("Ingresa el texto cifrado: ")
                k = int(input("Ingresa el desplazamiento k (entero): "))
                print("\nResultado Descifrado:", descifrar(texto, k))
                
            elif opcion == '3':
                texto = input("Ingresa el texto cifrado a interceptar: ")
                print("\nIniciando fuerza bruta...\n")
                ataque = fuerza_bruta(texto)
                for llave, texto_posible in ataque.items():
                    print(f"k = {llave:2d}: {texto_posible}")
                    
            elif opcion == '4':
                texto_original = "HOLA UNAL"
                k = 3
                cifrado = cifrar(texto_original, k)
                descifrado = descifrar(cifrado, k)
                
                print(f"\nTexto Original  : {texto_original}")
                print(f"Desplazamiento  : k = {k}")
                print(f"Texto Cifrado   : {cifrado}")
                print(f"Texto Descifrado: {descifrado}")
                print("\n=== ATAQUE DE FUERZA BRUTA (25 desplazamientos) ===")
                ataque = fuerza_bruta(cifrado)
                for llave, texto_posible in ataque.items():
                    marcador = " <-- (¡MENSAJE ENCONTRADO!)" if llave == k else ""
                    print(f"k = {llave:2d}: {texto_posible}{marcador}")
                    
            elif opcion == '0':
                print("\nSaliendo del programa...")
                break
            else:
                print("\n[!] Opción no válida. Inténtalo de nuevo.")
                
        except ValueError:
            print("\n[!] Error: El valor de desplazamiento k debe ser un número entero.")
        except KeyboardInterrupt:
            print("\n[!] Operación cancelada por el usuario. Saliendo...")
            break

