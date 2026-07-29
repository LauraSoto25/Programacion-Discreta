# Ejercicio 1: Cifrado César

## 1. ¿Qué problema resuelve el programa?
Permite ocultar un mensaje (cifrado) y recuperar el mensaje original (descifrado) con una clave compartida $k$. Asimismo, permite interceptar y recuperar mensajes cifrados de los cuales se desconoce la clave de cifrado mediante un ataque de fuerza bruta sobre todo el espacio de llaves del algoritmo.

## 2. ¿Qué idea matemática usa?
Utiliza **Aritmética Modular** en la estructura algebraica $\mathbb{Z}_{26}$ (el anillo de enteros módulo 26, correspondiente a las 26 letras del alfabeto latino sin 'Ñ').

Representando cada letra por su posición ordinal $x \in \{0, 1, \dots, 25\}$:
- **Función de Cifrado:**
  $$E(x, k) = (x + k) \pmod{26}$$
- **Función de Descifrado:**
  $$D(y, k) = (y - k) \pmod{26} \equiv (y + (-k)) \pmod{26}$$

## 3. ¿Cómo se ejecuta?
Desde el directorio raíz del repositorio (`Programacion-Discreta/`):

1. **Ejecutar el script principal:**
   ```bash
   python src/cripto/cesar.py
   ```
2. **Ejecutar las pruebas unitarias:**
   ```bash
   python -m unittest tests/test_cesar.py
   ```

## 4. ¿Qué pruebas se realizaron?
Se implementaron pruebas automatizadas en `tests/test_cesar.py` para validar:
- **Caso obligatorio:** Cifrar `"HOLA UNAL"` con $k=3$ obteniendo `"KROD XQDO"`.
- **Descifrado inverso:** Confirmar que $D(E(M, k), k) = M$.
- **Conservación de caracteres:** Verificación de preservación de mayúsculas, minúsculas, dígitos, espacios y caracteres de puntuación intactos.
- **Resiliencia de llaves:** Verificación de periodicidad con llaves $k < 0$ y $k > 26$.
- **Ataque de fuerza bruta:** Verificación de que las 25 variaciones son generadas y la clave correcta revela el texto legible.

## 5. Limitaciones de la solución
- El algoritmo se aplica exclusivamente sobre el rango de letras del alfabeto inglés ($A-Z, a-z$). Caracteres fuera del alfabeto (como la 'Ñ', tildes o símbolos) no se desplazan para mantener la definición estricta de $\mathbb{Z}_{26}$.
- El cifrado por sustitución monoalfabética es vulnerable al análisis de frecuencias de letras si el texto es lo suficientemente largo.

---

### Preguntas conceptuales obligatorias

#### ¿Por qué el descifrado usa el desplazamiento contrario?
Porque el descifrado es la función inversa del cifrado. Si al cifrar sumamos un desplazamiento $k$ al índice de la letra ($x + k$), para invertir el proceso debemos restar el mismo desplazamiento $k$. 

Por las propiedades de la aritmética modular:
$$(x + k - k) \pmod{26} \equiv x \pmod{26}$$
Restar $k$ equivale a sumar el inverso aditivo de $k$ módulo 26, lo cual significa retroceder $k$ posiciones en el alfabeto circular.

#### ¿Por qué el ataque de fuerza bruta es posible en este cifrado?
Porque el **espacio de llaves** $|\mathcal{K}|$ es extremadamente pequeño. En un alfabeto de 26 letras, solo existen 25 claves posibles de desplazamiento con efecto (excluyendo $k=0$ que deja el texto idéntico). Probar 25 hipótesis de llaves toma fracciones de milisegundo en una computadora moderna, permitiendo al atacante inspeccionar los 25 resultados e identificar de inmediato el texto legible en lenguaje natural.
