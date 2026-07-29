"""
Pruebas unitarias para el Ejercicio 4 (Ruta más corta con Dijkstra).
Ejecutar con: python -m unittest tests/test_dijkstra.py
"""

import unittest
import sys
import os

directorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if directorio_raiz not in sys.path:
    sys.path.insert(0, directorio_raiz)

from src.grafos.dijkstra import dijkstra, CIUDAD

class TestDijkstra(unittest.TestCase):

    def test_caso_minimo_obligatorio(self):
        """Prueba una ruta normal en el grafo quemado (CIUDAD)."""
        # Portal -> Centro (10) vs Portal -> Calle26 -> Centro (7)
        distancia, ruta = dijkstra(CIUDAD, "Portal", "Centro")
        self.assertEqual(distancia, 7)
        self.assertEqual(ruta, ["Portal", "Calle26", "Centro"])
        
        # Portal a Universidad:
        # Camino más corto: Portal(0) -> Calle26(5) -> Centro(7) -> Parque(14) -> Univ(16)
        # O también: Portal(0) -> Calle26(5) -> Museo(11) -> Univ(19) (es peor)
        # O también: Portal(0) -> Calle26(5) -> Centro(7) -> Biblioteca(10) -> Estadio(14) -> Univ(17) (peor que 16)
        distancia, ruta = dijkstra(CIUDAD, "Portal", "Universidad")
        self.assertEqual(distancia, 16)
        self.assertEqual(ruta, ["Portal", "Calle26", "Centro", "Parque", "Universidad"])

    def test_mismo_origen_y_destino(self):
        """La distancia a sí mismo debe ser 0 y la ruta solo contener el nodo."""
        distancia, ruta = dijkstra(CIUDAD, "Museo", "Museo")
        self.assertEqual(distancia, 0)
        self.assertEqual(ruta, ["Museo"])

    def test_nodos_desconectados(self):
        """Si un nodo es inalcanzable, la distancia es infinito y la ruta vacía."""
        grafo_desconectado = {
            "A": {"B": 1},
            "B": {"A": 1},
            "C": {}
        }
        distancia, ruta = dijkstra(grafo_desconectado, "A", "C")
        self.assertEqual(distancia, float('inf'))
        self.assertEqual(ruta, [])

    def test_pesos_negativos_lanzan_error(self):
        """Dijkstra no soporta pesos negativos, debe levantar excepción."""
        grafo_malo = {
            "A": {"B": -5},
            "B": {"A": 2}
        }
        with self.assertRaises(ValueError):
            dijkstra(grafo_malo, "A", "B")
            
    def test_nodos_inexistentes(self):
        """Si el origen o destino no existen en el grafo, retorna inf y lista vacía."""
        distancia, ruta = dijkstra(CIUDAD, "Atlantis", "Portal")
        self.assertEqual(distancia, float('inf'))
        self.assertEqual(ruta, [])

if __name__ == "__main__":
    unittest.main()
