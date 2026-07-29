# Ejercicio 3: MPC Básico (Calcular un promedio sin mostrar datos)

## 1. ¿Qué problema resuelve el programa?
Resuelve el problema de calcular operaciones agregadas (como la suma total y el promedio) a partir de datos privados que pertenecen a varios usuarios, garantizando que ninguna entidad externa ni los servidores participantes puedan conocer los datos individuales. Esto se simula con el cálculo del promedio de calificaciones de estudiantes sin revelar la nota de ningún estudiante a ningún servidor en particular.

## 2. ¿Qué idea matemática usa?
Utiliza la idea de **Secret Sharing** (Compartición de Secretos) aditivo sobre aritmética modular. 
Cada nota $x$ se divide en tres partes (o "fragmentos") $s_1, s_2, s_3$ mediante un módulo $M$ lo suficientemente grande de forma que:
$$s_3 \equiv (x - s_1 - s_2) \pmod{M}$$

**Ejemplo pequeño:**
Asumamos un módulo pequeño $M = 100$. Un estudiante saca $x = 42$.
- Elegimos dos números aleatorios en $[0, 99]$: $s_1 = 80$ y $s_2 = 15$.
- Calculamos el tercer fragmento: $s_3 = (42 - 80 - 15) \pmod{100} = (-53) \pmod{100} = 47$.
- El servidor 1 recibe `80`, el servidor 2 recibe `15`, el servidor 3 recibe `47`.
- Ninguno de los servidores, viendo solo su número, puede saber que la nota era 42 (por ejemplo, el Servidor 1 ve un 80, que ni siquiera está en la escala de notas 0-50, es puro ruido estadístico).
- Sin embargo, si al final los servidores suman sus partes, reconstruyen el secreto: $(80 + 15 + 47) \pmod{100} = 142 \pmod{100} = 42$.

Para $N$ estudiantes, la propiedad de linealidad de la suma modular garantiza que la suma de las sumas parciales es congruente a la suma de las notas originales.

## 3. ¿Cómo se ejecuta?
Desde el directorio raíz del repositorio (`Programacion-Discreta/`):

1. **Ejecutar el script principal (menú interactivo):**
   ```bash
   python src/cripto/mpc.py
   ```
2. **Ejecutar las pruebas unitarias:**
   ```bash
   python -m unittest tests/test_mpc.py
   ```

## 4. ¿Qué pruebas hicieron?
Se implementaron pruebas automatizadas en `tests/test_mpc.py` para verificar:
- **Caso obligatorio:** Notas `[40, 35, 50, 25]`. La simulación demuestra que se obtiene correctamente `suma=150` y `promedio=37.5`.
- **Validez Matemática de la Compartición:** Que la generación aleatoria de $s_1, s_2, s_3$ sí sume el secreto original módulo $M$.
- **Privacidad:** Que ninguno de los fragmentos aleatorios individuales coincida con la nota expuesta.
- **Límites Excedidos:** Verifica que el programa lance un error explícito si la suma real de las notas excede el valor $M$ (ya que en ese caso, el módulo "daría la vuelta" truncando la suma de modo incorrecto).

## 5. ¿Qué limitaciones tiene la solución?
- **Límite Teórico de la Suma:** El resultado de la suma debe ser estrictamente inferior a $M$. Si hay demasiados estudiantes, se necesita aumentar $M$ (en nuestra implementación $M=1000003$ soporta hasta $\approx 20,000$ notas de 50).
- **Colusión de Servidores:** La privacidad está garantizada solo si los servidores no colaboran entre ellos. Si los tres servidores (o incluso dos, en algunos escenarios si tuvieran acceso a otros parámetros) deciden unir su información, pueden reconstruir las notas individuales. Esto es una limitación estándar del protocolo aditivo si todos los participantes confabulan.
