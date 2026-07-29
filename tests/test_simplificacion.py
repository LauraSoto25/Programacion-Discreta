"""
Pruebas unitarias para el Ejercicio 8 (Simplificación Booleana).
Ejecutar con: python -m unittest tests/test_simplificacion.py
"""

import unittest
import sys
import os

directorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if directorio_raiz not in sys.path:
    sys.path.insert(0, directorio_raiz)

from src.boole.simplificacion import simplificar, comprobar_equivalencia, obtener_implicantes_primos, obtener_implicantes_esenciales, int_a_binario_str

class TestSimplificacion(unittest.TestCase):

    def test_caso_minimo_obligatorio(self):
        """Para 3 variables, probar la función con minitérminos {1, 3, 5, 7}. Esperado: C."""
        minterminos = [1, 3, 5, 7]
        num_vars = 3
        # 1: 001, 3: 011, 5: 101, 7: 111 -> Difieren en A y B, pero todos tienen C=1. 
        # La simplificación es C (la 3ra letra)
        resultado = simplificar(minterminos, num_vars)
        self.assertEqual(resultado, "C")
        
        # Verificar equivalencia
        minterminos_bin = {int_a_binario_str(m, num_vars) for m in minterminos}
        primos = obtener_implicantes_primos(minterminos_bin)
        esenciales = obtener_implicantes_esenciales(primos, minterminos_bin)
        self.assertTrue(comprobar_equivalencia(minterminos, num_vars, esenciales))

    def test_cuatro_variables(self):
        """Probar con 4 variables {0, 1, 2, 3}. Esperado: A'B'."""
        minterminos = [0, 1, 2, 3]
        num_vars = 4
        # 0000, 0001, 0010, 0011 -> C y D varían, A=0, B=0 constante. 
        # Esperado: A'B'
        resultado = simplificar(minterminos, num_vars)
        self.assertEqual(resultado, "A'B'")
        
        # Verificar equivalencia
        minterminos_bin = {int_a_binario_str(m, num_vars) for m in minterminos}
        primos = obtener_implicantes_primos(minterminos_bin)
        esenciales = obtener_implicantes_esenciales(primos, minterminos_bin)
        self.assertTrue(comprobar_equivalencia(minterminos, num_vars, esenciales))

    def test_funcion_constante_uno(self):
        """Si todos los minitérminos están presentes, la función es 1 constante."""
        minterminos = [0, 1, 2, 3, 4, 5, 6, 7]
        num_vars = 3
        resultado = simplificar(minterminos, num_vars)
        self.assertEqual(resultado, "1")

    def test_funcion_constante_cero(self):
        """Si no hay minitérminos, la función es 0 constante."""
        minterminos = []
        num_vars = 3
        resultado = simplificar(minterminos, num_vars)
        self.assertEqual(resultado, "0")
        
if __name__ == "__main__":
    unittest.main()
