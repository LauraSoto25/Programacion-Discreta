# Ejercicio 8: Simplificación Booleana (Hacer un circuito más barato)

## 1. ¿Qué problema resuelve el programa?
En electrónica digital, las expresiones lógicas complejas requieren un gran número de compuertas (AND, OR, NOT) para ser implementadas físicamente. Cada compuerta tiene un costo, ocupa espacio y añade retraso en la propagación de la señal. El programa resuelve el problema de la optimización: dada una función booleana original expresada mediante su lista completa de casos verdaderos (minitérminos), el programa encuentra la expresión mínima posible en formato Suma de Productos (SOP), ahorrando compuertas lógicas sin alterar el comportamiento.

## 2. ¿Qué idea matemática usa?
El programa utiliza el **Álgebra de Boole** y específicamente el concepto de **Adyacencia Lógica**. Dos minitérminos son lógicamente adyacentes si difieren en exactamente una variable. Por el teorema $X \cdot Y + X \cdot Y' = X$, la variable que cambia puede ser eliminada.

Para automatizar esto a gran escala, se usa el **Algoritmo de Quine-McCluskey (Método Tabular)**, el cual consta de dos partes matemáticas:
1. **Búsqueda de Implicantes Primos:** Agrupación exhaustiva de términos adyacentes hasta que no se puedan reducir más.
2. **Problema de Cobertura de Conjuntos (Set Cover):** De todos los implicantes primos encontrados, se usa un algoritmo de cobertura voraz para seleccionar el subconjunto mínimo (implicantes esenciales) que logre cubrir todos los minitérminos originales.

## 3. ¿Cómo se ejecuta?
Desde el directorio raíz del repositorio (`Programacion-Discreta/`):

1. **Ejecutar el script principal (CLI Interactivo):**
   ```bash
   python src/boole/simplificacion.py
   ```
2. **Ejecutar las pruebas unitarias:**
   ```bash
   python -m unittest tests/test_simplificacion.py
   ```

## 4. ¿Qué pruebas se realizaron?
Se implementaron pruebas unitarias en `tests/test_simplificacion.py`:
- **Caso obligatorio:** Función de 3 variables con minitérminos `{1, 3, 5, 7}`. El algoritmo agrupa exitosamente $m_1$ con $m_3$, $m_5$ con $m_7$, y finalmente ambos grupos para reducir la expresión a un solo término: `C` (la variable de menor peso), verificando además la equivalencia de su tabla de verdad (donde $C=1$).
- **Simplificación avanzada:** Función de 4 variables `{0, 1, 2, 3}`. Se redujo correctamente a `A'B'`.
- **Casos límite:** Cuando todos los minitérminos están presentes (resultado `1`) y cuando la lista está vacía (resultado `0`).

## 5. Limitaciones de la solución
- El algoritmo de Quine-McCluskey es **NP-Hard**. Aunque funciona maravillosamente para 3 o 4 variables (como se pide en este taller), el tiempo de ejecución y uso de memoria crece exponencialmente (en orden de $O(3^n/\sqrt{n})$). Para funciones de más de 10 variables, este código se volvería ineficiente; en la industria real se usan algoritmos heurísticos avanzados como Espresso.
- Para simplificar la implementación del "Set Cover", se usó una selección voraz. Aunque funciona bien para funciones pequeñas, no garantiza estrictamente la menor cantidad de implicantes en casos extremadamente complejos con implicantes redundantes cíclicos.

---

### Preguntas conceptuales obligatorias

#### ¿Qué significa un minitérmino?
Un minitérmino es una expresión lógica en forma de producto (AND) en la cual aparecen **todas** las variables de la función (afirmadas o negadas exactamente una vez). Cada minitérmino corresponde biunívocamente a **una única fila** en la tabla de verdad donde la función tiene un valor de $1$ (Verdadero). Por ejemplo, en 3 variables ($A, B, C$), el minitérmino $m_5$ corresponde al estado binario $101$, que lógicamente es $A \cdot B' \cdot C$.

#### ¿Por qué dos expresiones son equivalentes si tienen la misma tabla de verdad?
Porque la tabla de verdad representa de manera exhaustiva el dominio completo y discreto de una función booleana ($2^n$ estados posibles). Si para cada una de esas posibles combinaciones de entrada, dos expresiones booleanas distintas producen exactamente la misma salida (0 o 1), entonces las funciones modelan el mismo comportamiento lógico exacto (isomorfismo). La forma algebraica en la que estén escritas es simplemente una representación distinta, pero semántica y matemáticamente, son la misma función.
