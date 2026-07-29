"""
Pruebas unitarias para el MPC Básico (Ejercicio 3).
Ejecutar con: python -m unittest discover -s tests
"""

import unittest
import sys
import os

# Asegurar que el directorio raíz del repositorio (que contiene 'src') esté en sys.path
directorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if directorio_raiz not in sys.path:
    sys.path.insert(0, directorio_raiz)

from src.cripto.mpc import dividir_nota, simular_mpc, M_DEFAULT

class TestMPCBasico(unittest.TestCase):

    def test_caso_minimo_obligatorio(self):
        """Prueba con el caso [40, 35, 50, 25]. Suma debe ser 150 y promedio 37.5."""
        notas = [40, 35, 50, 25]
        suma, prom, _ = simular_mpc(notas, M_DEFAULT)
        self.assertEqual(suma, 150)
        self.assertEqual(prom, 37.5)

    def test_division_de_notas(self):
        """Verifica que los 3 fragmentos de una nota sumen la nota original módulo M."""
        nota = 42
        s1, s2, s3 = dividir_nota(nota, M_DEFAULT)
        suma_mod = (s1 + s2 + s3) % M_DEFAULT
        self.assertEqual(suma_mod, nota)

    def test_privacidad_servidores(self):
        """Verifica que ningún fragmento por sí solo revele la nota."""
        nota = 50
        s1, s2, s3 = dividir_nota(nota, M_DEFAULT)
        # Es estadísticamente improbable que un fragmento sea igual a la nota si M es grande
        self.assertNotEqual(s1, nota)
        self.assertNotEqual(s2, nota)
        
    def test_lista_vacia(self):
        """Verifica el comportamiento con una lista vacía de notas."""
        notas = []
        suma, prom, parciales = simular_mpc(notas, M_DEFAULT)
        self.assertEqual(suma, 0)
        self.assertEqual(prom, 0.0)
        self.assertEqual(parciales, [0, 0, 0])

    def test_excepcion_modulo(self):
        """Verifica que se lance excepción si la suma supera M."""
        # Cada nota es 50. Si hay 21000 notas, la suma es 1050000 > 1000003
        notas = [50] * 21000
        with self.assertRaises(ValueError):
            simular_mpc(notas, M_DEFAULT)

if __name__ == "__main__":
    unittest.main()
