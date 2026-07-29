"""
Pruebas unitarias para el Ejercicio 5 (Cierre de Estación / Grafos).
Ejecutar con: python -m unittest discover -s tests
"""

import unittest
import sys
import os

directorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if directorio_raiz not in sys.path:
    sys.path.insert(0, directorio_raiz)

from src.grafos.cierre_estacion import Grafo, construir_grafo_prueba, simular_cierre

class TestCierreEstacion(unittest.TestCase):

    def setUp(self):
        self.grafo = construir_grafo_prueba()
        
    def test_dijkstra_ruta_corta(self):
        """Verifica que Dijkstra encuentre la distancia y ruta correcta (antes de cierre)."""
        dist, ruta = self.grafo.dijkstra("Portal_Norte", "Ricaurte")
        # Norte -> Calle_100 -> Calle_72 -> Ricaurte = 10 + 8 + 12 = 30
        # Norte -> Calle_100 -> Ricaurte = 10 + 20 = 30
        # Ambas miden 30.
        self.assertEqual(dist, 30)
        self.assertTrue(ruta == ["Portal_Norte", "Calle_100", "Calle_72", "Ricaurte"] or 
                        ruta == ["Portal_Norte", "Calle_100", "Ricaurte"])

    def test_eliminar_vertice_aislamiento(self):
        """Verifica que eliminar un vértice clave desconecte partes del grafo (si es el único puente)."""
        g = Grafo()
        g.agregar_arista("A", "B", 10)
        g.agregar_arista("B", "C", 10)
        # Ruta A -> C = 20
        dist, _ = g.dijkstra("A", "C")
        self.assertEqual(dist, 20)
        
        # Eliminar puente B
        g.eliminar_vertice("B")
        dist_aislado, _ = g.dijkstra("A", "C")
        self.assertEqual(dist_aislado, float('inf'))

    def test_simulacion_reporte(self):
        """Verifica que simular_cierre reporte las distancias antes y después."""
        pares = [("Banderas", "Centro")]
        # Banderas -> Ricaurte -> Centro = 10 + 8 = 18
        
        reporte = simular_cierre(self.grafo, "Ricaurte", pares)
        self.assertEqual(len(reporte), 1)
        res = reporte[0]
        self.assertEqual(res["dist_antes"], 18)
        
        # Si eliminamos Ricaurte, la ruta alterna es:
        # Banderas -> Portal_Sur -> Centro = 15 + 25 = 40
        self.assertEqual(res["dist_despues"], 40)
        self.assertEqual(res["diferencia"], 22)
        self.assertEqual(res["estado"], "AUMENTÓ")
        
    def test_pares_desconectados(self):
        """Verifica el estado DESCONECTADO."""
        g = Grafo()
        g.agregar_arista("X", "Y", 5)
        g.agregar_arista("Y", "Z", 5)
        
        pares = [("X", "Z")]
        reporte = simular_cierre(g, "Y", pares)
        self.assertEqual(reporte[0]["estado"], "DESCONECTADO")
        self.assertEqual(reporte[0]["dist_despues"], float('inf'))

if __name__ == "__main__":
    unittest.main()
