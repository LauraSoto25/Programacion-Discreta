# Ejercicio 9: Entropía de Shannon (Medir Información)

## 1. ¿Qué problema resuelve el programa?
Permite medir matemáticamente cuánta "información" o "incertidumbre" contiene un mensaje. Un mensaje muy predecible (repetitivo) contiene muy poca información por carácter, mientras que un mensaje completamente aleatorio o variado contiene mucha información, pues cada símbolo es una sorpresa. Esto es fundamental para problemas de compresión de datos y criptografía.

## 2. ¿Qué idea matemática usa?
Utiliza el concepto de **Entropía de Shannon**, fundamentado en la teoría de la información y la probabilidad. 
Dada una variable aleatoria discreta (los símbolos de un alfabeto) con una función de masa de probabilidad $p(x)$, la entropía $H$ se define como:
$$H = -\sum_{i} p_i \log_2 (p_i)$$
Donde $p_i$ es la probabilidad de aparición del símbolo $i$. El resultado se mide en **bits por símbolo**. Si un símbolo tiene una probabilidad de aparición del 100% ($p=1$), su contribución a la entropía es $1 \cdot \log_2(1) = 0$, significando que no aporta incertidumbre.

## 3. ¿Cómo se ejecuta?
Desde el directorio raíz del repositorio (`Programacion-Discreta/`):

1. **Ejecutar el programa con el menú interactivo:**
   ```bash
   python src/boole/shannon.py
   ```
2. **Ejecutar las pruebas unitarias:**
   ```bash
   python -m unittest tests/test_shannon.py
   ```

## 4. ¿Qué pruebas hicieron?
Se implementaron pruebas en `tests/test_shannon.py` verificando:
- **Entropía Nula:** Un texto repetitivo compuesto por un solo carácter (ej. `"AAAAAA"`) tiene entropía exactamente $0.0$, ya que no hay incertidumbre sobre cuál será el siguiente carácter.
- **Entropía Binaria Perfecta:** Un texto de dos caracteres alternados y equiprobables (ej. `"ABAB"`) tiene entropía exactamente $1.0$ bit, equivalente a lanzar una moneda justa.
- **Comparación y Probabilidades:** Verificación de que un texto heterogéneo (ej. `"ABCDEFGHI"`) produce una entropía mayor que un texto homogéneo (ej. `"AAAAAAAAB"`).
- **Control de errores:** Manejo correcto de strings vacíos devolviendo $0.0$.

## 5. ¿Qué limitaciones tiene la solución?
El cálculo asume que los símbolos son emitidos por una fuente "sin memoria" (Modelos de orden 0). Es decir, asume que la probabilidad de un carácter es independiente del carácter anterior. En el lenguaje natural real (como el español), la aparición de una "U" después de una "Q" es casi del 100%, por lo que la verdadera entropía del lenguaje es mucho menor que la calculada simplemente contando frecuencias sueltas.

---

### Pregunta de Documentación

#### ¿Por qué la entropía mide incertidumbre y no simplemente longitud del texto?
La longitud del texto solo nos dice cuánto espacio físico ocupa una cadena de caracteres, pero no nos dice nada sobre su contenido. Si tenemos un texto de un millón de letras "A", su longitud es enorme, pero su **incertidumbre** es cero: si intentamos adivinar la siguiente letra, estaremos 100% seguros de que será una "A". Como no hay sorpresa, no hay información nueva.

La entropía, en cambio, mide qué tan "sorprendente" o difícil de predecir es cada símbolo en promedio. Si el texto tiene una alta variedad de símbolos distribuidos de forma uniforme, no sabremos con certeza qué símbolo viene a continuación. Por lo tanto, la entropía mide la **calidad o densidad de la información** por símbolo (incertidumbre), desvinculándola de la cantidad bruta de símbolos (longitud).
