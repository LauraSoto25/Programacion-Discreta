"""
Pruebas unitarias para el Ejercicio 6 (Coloreo de grafos).
Ejecutar con: python -m unittest tests/test_coloreo.py
"""

import unittest
import sys
import os

directorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if directorio_raiz not in sys.path:
    sys.path.insert(0, directorio_raiz)

from src.grafos.coloreo import coloreo_voraz, verificar_coloreo, MATERIAS_CONFLICTO

class TestColoreo(unittest.TestCase):

    def test_caso_minimo_obligatorio(self):
        """El grafo de 11 nodos (materias) debe ser coloreado válidamente."""
        asignacion = coloreo_voraz(MATERIAS_CONFLICTO)
        self.assertTrue(verificar_coloreo(MATERIAS_CONFLICTO, asignacion))
        self.assertEqual(len(asignacion), 11)

    def test_grafo_completo(self):
        """Un grafo completo K_4 requiere exactamente 4 colores."""
        k4 = {
            "A": {"B", "C", "D"},
            "B": {"A", "C", "D"},
            "C": {"A", "B", "D"},
            "D": {"A", "B", "C"}
        }
        asignacion = coloreo_voraz(k4)
        self.assertTrue(verificar_coloreo(k4, asignacion))
        colores_usados = set(asignacion.values())
        self.assertEqual(len(colores_usados), 4)

    def test_grafo_bipartito_estrella(self):
        """Un grafo estrella es bipartito y requiere exactamente 2 colores."""
        estrella = {
            "Centro": {"P1", "P2", "P3", "P4"},
            "P1": {"Centro"},
            "P2": {"Centro"},
            "P3": {"Centro"},
            "P4": {"Centro"}
        }
        asignacion = coloreo_voraz(estrella)
        self.assertTrue(verificar_coloreo(estrella, asignacion))
        colores_usados = set(asignacion.values())
        self.assertEqual(len(colores_usados), 2)
        
    def test_verificador_detecta_conflictos(self):
        """El verificador debe fallar si manualmente introducimos un conflicto."""
        grafo = {
            "A": {"B"},
            "B": {"A"}
        }
        asignacion_invalida = {"A": 0, "B": 0}
        self.assertFalse(verificar_coloreo(grafo, asignacion_invalida))

if __name__ == "__main__":
    unittest.main()
