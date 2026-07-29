"""
Pruebas unitarias para el Ejercicio 9 (Entropía de Shannon).
Ejecutar con: python -m unittest discover -s tests
"""

import unittest
import sys
import os

directorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if directorio_raiz not in sys.path:
    sys.path.insert(0, directorio_raiz)

from src.boole.shannon import calcular_frecuencias, calcular_probabilidades, calcular_entropia, comparar_textos

class TestShannon(unittest.TestCase):

    def test_frecuencias_probabilidades(self):
        """Verifica que las frecuencias y probabilidades se calculen correctamente."""
        texto = "AABB"
        freqs = calcular_frecuencias(texto)
        probs = calcular_probabilidades(texto)
        
        self.assertEqual(freqs['A'], 2)
        self.assertEqual(freqs['B'], 2)
        
        self.assertAlmostEqual(probs['A'], 0.5)
        self.assertAlmostEqual(probs['B'], 0.5)

    def test_entropia_cero(self):
        """Un texto con un solo símbolo repetido tiene entropía 0 (ninguna incertidumbre)."""
        texto = "AAAAAA"
        entropia = calcular_entropia(texto)
        self.assertAlmostEqual(entropia, 0.0)

    def test_entropia_moneda(self):
        """Un texto con dos símbolos equiprobables tiene entropía de 1 bit."""
        texto = "ABAB"
        entropia = calcular_entropia(texto)
        self.assertAlmostEqual(entropia, 1.0)
        
    def test_comparacion_textos(self):
        """Verifica la lógica comparativa entre un texto repetitivo y uno variado."""
        repetitivo = "AAAAAAAAB"
        variado = "ABCDEFGHI"
        
        h1, h2, explicacion = comparar_textos(repetitivo, variado)
        self.assertGreater(h2, h1)
        self.assertIn("Texto 2", explicacion)

    def test_texto_vacio(self):
        """Verifica el comportamiento con un texto vacío."""
        self.assertEqual(calcular_entropia(""), 0.0)
        self.assertEqual(calcular_frecuencias(""), {})

if __name__ == "__main__":
    unittest.main()
