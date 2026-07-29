"""
Pruebas unitarias para el Ejercicio 10 (Simulador Cuántico).
Ejecutar con: python -m unittest tests/test_simulador.py
"""

import unittest
import sys
import os
import math

directorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if directorio_raiz not in sys.path:
    sys.path.insert(0, directorio_raiz)

from src.cuantica.simulador import (
    crear_qubit, aplicar_compuerta, calcular_probabilidades, 
    simular_mediciones, COMPUERTA_X, COMPUERTA_Z, COMPUERTA_H
)

class TestSimulador(unittest.TestCase):

    def assertComplexAlmostEqual(self, c1: complex, c2: complex, places=5):
        """Método auxiliar para comparar números complejos con tolerancia por flotantes."""
        self.assertAlmostEqual(c1.real, c2.real, places=places)
        self.assertAlmostEqual(c1.imag, c2.imag, places=places)

    def test_x_sobre_cero(self):
        """Probar que X|0> = |1>"""
        q = crear_qubit(0)
        q_final = aplicar_compuerta(COMPUERTA_X, q)
        
        # El estado debe ser [0, 1]
        self.assertComplexAlmostEqual(q_final[0], 0 + 0j)
        self.assertComplexAlmostEqual(q_final[1], 1 + 0j)
        
        prob_0, prob_1 = calcular_probabilidades(q_final)
        self.assertEqual(prob_0, 0.0)
        self.assertEqual(prob_1, 1.0)

    def test_h_sobre_cero(self):
        """Probar que H|0> da probabilidades 50% y 50%"""
        q = crear_qubit(0)
        q_final = aplicar_compuerta(COMPUERTA_H, q)
        
        prob_0, prob_1 = calcular_probabilidades(q_final)
        self.assertAlmostEqual(prob_0, 0.5, places=5)
        self.assertAlmostEqual(prob_1, 0.5, places=5)

    def test_hh_sobre_cero(self):
        """Probar que HH|0> = |0> (revierte al estado inicial)"""
        q = crear_qubit(0)
        q_temp = aplicar_compuerta(COMPUERTA_H, q)
        q_final = aplicar_compuerta(COMPUERTA_H, q_temp)
        
        # Debe ser [1, 0] nuevamente
        self.assertComplexAlmostEqual(q_final[0], 1 + 0j)
        self.assertComplexAlmostEqual(q_final[1], 0 + 0j)

    def test_z_sobre_uno(self):
        """Probar que Z|1> = -|1>"""
        q = crear_qubit(1)
        q_final = aplicar_compuerta(COMPUERTA_Z, q)
        
        # Debe ser [0, -1]
        self.assertComplexAlmostEqual(q_final[0], 0 + 0j)
        self.assertComplexAlmostEqual(q_final[1], -1 + 0j)
        
        # Pero la probabilidad sigue siendo 100% para |1>
        prob_0, prob_1 = calcular_probabilidades(q_final)
        self.assertEqual(prob_0, 0.0)
        self.assertEqual(prob_1, 1.0)
        
    def test_simulacion_mediciones(self):
        """Probar que simular 1000 veces sobre H|0> da valores estadísticamente aceptables"""
        q = aplicar_compuerta(COMPUERTA_H, crear_qubit(0))
        c_0, c_1 = simular_mediciones(q, 1000)
        
        # Comprobar que sumen 1000
        self.assertEqual(c_0 + c_1, 1000)
        
        # Comprobar que estén cerca del 50% (entre 400 y 600 es un rango muy seguro estadísticamente)
        self.assertTrue(400 <= c_0 <= 600)
        self.assertTrue(400 <= c_1 <= 600)

if __name__ == "__main__":
    unittest.main()
