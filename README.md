# Taller 3 - Programación Discreta

**Asignatura:** Matemáticas Discretas I  
**Docente:** Jhoan Sebastian Tenjo García  
**Universidad Nacional de Colombia**  

## Estructura del Proyecto

```
Programacion-Discreta/
├── README.md               # Descripción general e instrucciones de ejecución
├── requirements.txt        # Dependencias del proyecto (Librerías estándar de Python)
├── src/                    # Código fuente de los 10 ejercicios
│   ├── __init__.py
│   ├── cripto/             # Bloque A: Criptografía (César, RSA, MPC)
│   │   ├── __init__.py
│   │   └── cesar.py
│   ├── grafos/             # Bloque B: Grafos (Dijkstra, Cierre estación, Coloreo)
│   │   └── __init__.py
│   ├── boole/              # Bloque C: Álgebra de Boole (Tablas de verdad, Quine-McCluskey)
│   │   └── __init__.py
│   └── cuantica/           # Bloque C: Simulador cuántico (Qubits, Compuertas X, Z, H)
│       └── __init__.py
├── tests/                  # Pruebas unitarias automatizadas
│   ├── __init__.py
│   └── test_cesar.py
└── docs/                   # Documentación explicativa en Markdown / PDF
    └── 01_cesar.md
```

## Requisitos e Instalación

El proyecto está desarrollado en **Python 3.10+** utilizando librerías estándar. No requiere dependencias externas obligatorias para la ejecución básica.

## Instrucciones de Ejecución

Para ejecutar las soluciones y sus pruebas, situarse en la raíz del repositorio (`Programacion-Discreta`):

### 1. Cifrado César (Ejercicio 1)
```bash
python src/cripto/cesar.py
```

### Ejecución de Pruebas Unitarias
Para correr todas las pruebas del proyecto:
```bash
python -m unittest discover -s tests
```
O para probar un archivo específico:
```bash
python -m unittest tests/test_cesar.py
```