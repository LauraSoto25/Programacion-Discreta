# Ejercicio 2: RSA de Juguete

## 1. ¿Qué problema resuelve el programa?
El programa simula el funcionamiento básico del sistema criptográfico asimétrico **RSA** (Rivest, Shamir, Adleman). A diferencia de los métodos simétricos como el Cifrado César (donde la misma llave cifra y descifra), RSA resuelve el problema de la distribución segura de claves mediante el uso de dos llaves distintas:
- Una **llave pública** $(e, n)$ para cifrar el mensaje.
- Una **llave privada** $(d, n)$ para descifrar el mensaje, la cual no puede deducirse fácilmente de la llave pública.

Este programa no está destinado a usarse en seguridad real debido a que maneja números enteros pequeños que son fácilmente factorizables.

## 2. ¿Qué idea matemática usa?
RSA fundamenta su seguridad en la dificultad computacional de factorizar el producto de dos números primos grandes y en propiedades clave de la **Aritmética Modular**.

Los pasos matemáticos implementados son:
1. **Selección de primos:** Se escogen dos números primos $p$ y $q$. Se calcula el módulo $n = p \times q$.
2. **Función indicatriz de Euler $\phi(n)$:** Se calcula $\phi(n) = (p - 1)(q - 1)$. Esto cuenta cuántos números menores a $n$ son coprimos con $n$.
3. **Exponente público ($e$):** Se escoge un número $e$ coprimo con $\phi(n)$, lo cual se verifica matemáticamente asegurando que $\gcd(e, \phi(n)) = 1$.
4. **Exponente privado ($d$) y Algoritmo de Euclides Extendido:** Para calcular la llave privada $d$, se busca el **inverso modular** de $e$ módulo $\phi(n)$. Se implementó manualmente el Algoritmo de Euclides Extendido para encontrar los coeficientes $x, y$ tales que $e \cdot x + \phi(n) \cdot y = \gcd(e, \phi(n)) = 1$. Entonces, $d \equiv x \pmod{\phi(n)}$.

Al cifrar un mensaje $M$, calculamos la congruencia:
$$C \equiv M^e \pmod{n}$$
Y por el Teorema de Euler, al descifrar garantizamos que:
$$C^d \equiv (M^e)^d \equiv M^{ed} \equiv M^{1 + k\phi(n)} \equiv M \pmod{n}$$

## 3. ¿Cómo se ejecuta?
Desde el directorio raíz del repositorio (`Programacion-Discreta/`):

1. **Ejecutar el script principal (CLI Interactivo):**
   ```bash
   python src/cripto/rsa.py
   ```
2. **Ejecutar las pruebas unitarias:**
   ```bash
   python -m unittest tests/test_rsa.py
   ```

## 4. ¿Qué pruebas se realizaron?
Se implementaron diversas pruebas automatizadas en `tests/test_rsa.py` utilizando el framework `unittest`:
- **Caso mínimo obligatorio:** $p=61, q=53, e=17, M=65$. El programa calcula correctamente que $n=3233, \phi(n)=3120, d=2753$. El texto cifrado es $C=2790$ y el texto descifrado es correctamente $M=65$.
- **Algoritmo de Euclides Extendido:** Verificación del cálculo del máximo común divisor y los coeficientes de Bezout ($a \cdot x + b \cdot y = \gcd(a, b)$).
- **Control de excepciones (Exponente inválido):** Verificación de que si el usuario proporciona un $e$ donde $\gcd(e, \phi(n)) \neq 1$, el programa detecta que el inverso modular no existe y lanza un `ValueError`.
- **Integridad de llaves y mensajes:** Pruebas para asegurar que $M < n$ para prevenir corrupción durante el cálculo de la congruencia modular.

## 5. Limitaciones de la solución
- **Seguridad trivial (RSA de juguete):** El programa admite números enteros pequeños para $p$ y $q$. En el mundo real, los números deben ser de 2048 a 4096 bits. Si $n$ es pequeño, es vulnerable a ataques de fuerza bruta o de factorización (como la criba cuadrática).
- **Exponenciación en texto claro (No Padding):** El programa cifra mensajes numéricos directos (Texto Plano Estándar) de forma determinista. Un ataque de texto cifrado escogido podría deducir relaciones fácilmente. RSA en el mundo real siempre va acompañado de un esquema de relleno (Padding) como OAEP.
