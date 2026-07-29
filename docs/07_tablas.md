# Ejercicio 7: Tablas de Verdad y Circuitos Lógicos

## 1. ¿Qué problema resuelve el programa?
Permite evaluar y visualizar exhaustivamente todas las posibles salidas de un sistema lógico binario a partir de todas las combinaciones posibles de sus entradas. Asimismo, provee una forma de evaluar puntualmente casos concretos (por ejemplo, para depurar una sola condición en particular sin generar toda la tabla).

## 2. ¿Qué idea matemática usa?
Se basa en el **Álgebra de Boole** y la combinatoria discreta.
Una expresión booleana de $n$ variables discretas (donde cada variable toma valores en $\{0, 1\}$) tiene asociadas exactamente $2^n$ combinaciones posibles en su dominio, lo cual forma el conjunto $\{0, 1\} \times \{0, 1\} \times \dots \times \{0, 1\}$.

El programa utiliza un producto cartesiano para garantizar la generación secuencial y ordenada de todo el dominio, aplicando los operadores formales del álgebra proposicional:
- **AND ($\land$)**: Intersección o producto lógico.
- **OR ($\lor$)**: Unión o suma lógica incluyente.
- **NOT ($\neg$)**: Complemento lógico o negación.
- **XOR ($\oplus$)**: Unión lógica excluyente (se evalúa matemáticamente como suma módulo 2 o desigualdad estricta).

## 3. ¿Cómo se ejecuta?
Desde el directorio raíz del repositorio (`Programacion-Discreta/`):

1. **Ejecutar el programa con el menú interactivo:**
   ```bash
   python src/boole/tablas.py
   ```
2. **Ejecutar las pruebas unitarias:**
   ```bash
   python -m unittest tests/test_tablas.py
   ```

## 4. ¿Qué pruebas hicieron?
Se implementaron pruebas estrictas en `tests/test_tablas.py` verificando:
- **Exactitud Lógica y Precedencia:** Se evaluaron casos puntuales de las tres expresiones exigidas por el profesor para asegurar que los operadores nativos (`and`, `or`, `not`, `^`) respetan el álgebra booleana (especialmente el XOR y la negación combinada en $(A \lor B) \land (\neg A \lor C)$).
- **Completitud del Dominio:** Se validó de manera automatizada que el generador de la tabla para 3 variables siempre construya exactamente $2^3 = 8$ filas, sin faltantes ni duplicados, y que la primera fila evaluada ($000$) concuerde con el resultado esperado manualmente.

## 5. ¿Qué limitaciones tiene la solución?
- **Escalamiento Exponencial ($O(2^n)$):** El programa genera las tablas evaluando cada estado uno por uno. Para 3 o 4 variables se resuelve instantáneamente (8 a 16 iteraciones). Sin embargo, si se evaluara un circuito real de 32 variables, la tabla generaría $2^{32}$ combinaciones (más de 4 mil millones de filas), colapsando el tiempo de ejecución y la consola debido a la limitante inherente de la fuerza bruta en espacios combinatorios gigantescos.

---

### Pregunta de Documentación

#### ¿Cómo se relaciona una tabla de verdad con un circuito lógico?
Una tabla de verdad actúa como el **contrato conductual o la especificación de diseño** de un circuito lógico digital. 

Mientras que la tabla nos dice *el qué* (el mapa exacto de "si entran estos voltajes, este debe ser el voltaje de salida"), el circuito lógico es *el cómo* se implementa eso físicamente mediante componentes semiconductores (transistores agrupados en compuertas AND, OR, NOT).

Adicionalmente, hay una correspondencia bidireccional perfecta: cualquier tabla de verdad, por caótica que parezca, puede convertirse automáticamente en un circuito físico. Esto se logra tomando todas las filas cuyo resultado es `1`, convirtiendo cada una en una compuerta `AND` (conocido como **mintérmino**), y uniendo todos esos bloques con una gran compuerta `OR` (suma de productos). Esta es la base matemática por la cual las computadoras físicas modernas funcionan y fue descrita originalmente por Claude Shannon en su aplicación del álgebra de Boole a relés electromecánicos.
