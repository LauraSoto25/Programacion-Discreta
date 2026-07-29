# Ejercicio 10: Simulador Cuántico (Bits, Qubits y Mediciones)

## 1. ¿Qué problema resuelve el programa?
En la computación clásica, los bits solo pueden estar en estados deterministas 0 o 1. La computación cuántica introduce el "Qubit", que puede existir en una superposición de 0 y 1 simultáneamente hasta que es medido. El problema que resuelve este programa es proveer una plataforma interactiva, matemática y simulada, para entender visualmente cómo el vector estado de un qubit se transforma al pasar por circuitos cuánticos (secuencias de compuertas lógicas como X, Z y H) sin necesidad de acceder a hardware cuántico real.

## 2. ¿Qué idea matemática usa?
El modelo matemático de la computación cuántica se fundamenta en el **Álgebra Lineal** sobre el cuerpo de los **Números Complejos**:
- **Estado (Qubit):** Se representa como un vector columna unitario $|\psi\rangle = \begin{pmatrix} \alpha \\ \beta \end{pmatrix}$, donde $\alpha, \beta \in \mathbb{C}$ y $|\alpha|^2 + |\beta|^2 = 1$.
- **Compuertas:** Son transformaciones lineales representadas por **Matrices Unitarias** de 2x2.
- **Evolución:** Aplicar una compuerta es simplemente multiplicar la matriz 2x2 por el vector estado 2x1.
- **Regla de Born (Medición):** La probabilidad teórica de medir el estado $|0\rangle$ es exactamente $|\alpha|^2$, y la de medir $|1\rangle$ es $|\beta|^2$.

## 3. ¿Cómo se ejecuta?
Desde el directorio raíz del repositorio (`Programacion-Discreta/`):

1. **Ejecutar el simulador interactivo:**
   ```bash
   python src/cuantica/simulador.py
   ```
2. **Ejecutar las pruebas unitarias:**
   ```bash
   python -m unittest tests/test_simulador.py
   ```

## 4. ¿Qué pruebas se realizaron?
Se implementaron pruebas matemáticas estrictas en `tests/test_simulador.py` usando aserciones de casi-igualdad para flotantes (`assertAlmostEqual`):
- **Obligatoria 1 ($X|0\rangle = |1\rangle$):** Se verificó que la compuerta NOT invierte correctamente el vector.
- **Obligatoria 2 ($H|0\rangle \to 50/50$):** Se calculó que las probabilidades finales son matemáticamente $0.5$ y $0.5$.
- **Obligatoria 3 ($HH|0\rangle = |0\rangle$):** Se demostró la naturaleza unitaria e involutiva de Hadamard, devolviendo el vector original tras doble aplicación.
- **Simulación Empírica:** Se validó que al realizar 1000 iteraciones aleatorias bajo la distribución de probabilidad generada por Hadamard, los resultados de conteo siempre caen dentro de un intervalo estadísticamente confiable (aproximadamente 500 veces cada uno).

## 5. Limitaciones de la solución
- Este programa simula **un solo qubit**. Para simular sistemas complejos de múltiples qubits entrelazados, la dimensión del vector de estado crece de forma exponencial ($2^n$), lo que hace que simuladores clásicos agoten la memoria RAM rápidamente a partir de los 40-50 qubits.

---

### Preguntas conceptuales obligatorias

#### ¿Cuál es la diferencia entre probabilidad cuántica simulada y la ejecución en un computador cuántico real?
1. **El Origen de la Aleatoriedad:** En nuestra simulación clásica de Python, las probabilidades se calculan matemáticamente (determinismo analítico) y luego las "mediciones" se fingen extrayendo números pseudoaleatorios de un generador de software (PRNG, clásico y determinista). En un computador cuántico real, el colapso de la función de onda al medir es un **fenómeno físico de verdadera aleatoriedad fundamental**, dictado por las leyes del universo a nivel subatómico.
2. **Descoherencia y Ruido:** Nuestra simulación es matemática y computacionalmente "perfecta". El estado evoluciona sin fricción de acuerdo a las matrices. En el hardware cuántico real, los qubits sufren "descoherencia" y errores físicos al interactuar térmicamente con el ambiente exterior, lo que introduce ruido en las lecturas probabilísticas empíricas reales.
