"""
Pruebas unitarias para el Ejercicio 7 (Tablas de Verdad).
Ejecutar con: python -m unittest discover -s tests
"""

import unittest
import sys
import os

directorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if directorio_raiz not in sys.path:
    sys.path.insert(0, directorio_raiz)

from src.boole.tablas import (
    expresion_1, expresion_2, expresion_3,
    evaluar_entrada_concreta, generar_tabla_verdad
)

class TestTablasDeVerdad(unittest.TestCase):

    def test_expresion_1(self):
        """Verifica (A ∧ B) ∨ (¬C)"""
        # A=True, B=True, C=True => (V and V) or (F) = V
        self.assertTrue(expresion_1(True, True, True))
        # A=False, B=True, C=True => (F and V) or (F) = F
        self.assertFalse(expresion_1(False, True, True))
        # A=False, B=False, C=False => (F and F) or (V) = V
        self.assertTrue(expresion_1(False, False, False))

    def test_expresion_2(self):
        """Verifica (A ⊕ B) ∧ C"""
        # A=True, B=False, C=True => (V XOR F) and V = V and V = V
        self.assertTrue(expresion_2(True, False, True))
        # A=True, B=True, C=True => (V XOR V) and V = F and V = F
        self.assertFalse(expresion_2(True, True, True))
        # A=False, B=True, C=False => (F XOR V) and F = V and F = F
        self.assertFalse(expresion_2(False, True, False))

    def test_expresion_3(self):
        """Verifica (A ∨ B) ∧ (¬A ∨ C)"""
        # A=True, B=False, C=True => (V or F) and (F or V) = V and V = V
        self.assertTrue(expresion_3(True, False, True))
        # A=True, B=True, C=False => (V or V) and (F or F) = V and F = F
        self.assertFalse(expresion_3(True, True, False))
        # A=False, B=False, C=True => (F or F) and (V or V) = F and V = F
        self.assertFalse(expresion_3(False, False, True))
        
    def test_evaluar_entrada_concreta(self):
        """Verifica la función envoltorio para evaluación manual."""
        res = evaluar_entrada_concreta(expresion_1, False, False, False)
        self.assertEqual(res, True)

    def test_generador_tabla(self):
        """Verifica que la tabla genere 2^3 = 8 filas para expresiones de 3 variables."""
        tabla = generar_tabla_verdad("Test Expr 1", expresion_1, num_vars=3)
        self.assertEqual(len(tabla), 8)
        
        # El primer elemento de la tabla es la combinación F,F,F
        combinacion_0, res_0 = tabla[0]
        self.assertEqual(combinacion_0, (False, False, False))
        self.assertEqual(res_0, True)  # Para la expr 1: (F and F) or (not F) = True

if __name__ == "__main__":
    unittest.main()
