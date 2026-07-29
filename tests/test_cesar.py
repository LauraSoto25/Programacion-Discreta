"""
Pruebas unitarias para el Cifrado César (Ejercicio 1).
Ejecutar con: python -m unittest discover -s tests
o con: python -m unittest tests/test_cesar.py
"""

import unittest
import sys
import os

# Asegurar que el directorio raíz del repositorio (que contiene 'src') esté en sys.path
directorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if directorio_raiz not in sys.path:
    sys.path.insert(0, directorio_raiz)

from src.cripto.cesar import cifrar, descifrar, fuerza_bruta

class TestCifradoCesar(unittest.TestCase):

    def test_caso_minimo_obligatorio(self):
        """Caso de prueba obligatorio según enunciado: 'HOLA UNAL' con k=3 resulta en 'KROD XQDO'."""
        texto = "HOLA UNAL"
        k = 3
        esperado = "KROD XQDO"
        self.assertEqual(cifrar(texto, k), esperado)

    def test_descifrado(self):
        """Verifica que el descifrado recupere el mensaje original."""
        texto_cifrado = "KROD XQDO"
        k = 3
        esperado = "HOLA UNAL"
        self.assertEqual(descifrar(texto_cifrado, k), esperado)

    def test_respeto_de_caracteres_y_mayusculas_minusculas(self):
        """Verifica que mantenga espacios, signos, números y preserve mayúsculas/minúsculas."""
        texto = "¡Hola, UNAL 2026!"
        k = 5
        # H -> M, o -> t, l -> q, a -> f => Mtqf
        # U -> Z, N -> S, A -> F, L -> Q => ZSFQ
        esperado = "¡Mtqf, ZSFQ 2026!"
        self.assertEqual(cifrar(texto, k), esperado)
        self.assertEqual(descifrar(esperado, k), texto)

    def test_fuerza_bruta(self):
        """Verifica que el ataque de fuerza bruta genere las 25 opciones y contenga el mensaje correcto."""
        cifrado = "KROD XQDO"
        resultados = fuerza_bruta(cifrado)
        self.assertEqual(len(resultados), 25)
        self.assertIn(3, resultados)
        self.assertEqual(resultados[3], "HOLA UNAL")

    def test_desplazamiento_grande_y_negativo(self):
        """Verifica la periodicidad del cifrado (k = 29 es equivalente a k = 3)."""
        texto = "PRUEBA"
        self.assertEqual(cifrar(texto, 29), cifrar(texto, 3))
        self.assertEqual(cifrar(texto, -3), descifrar(texto, 3))

if __name__ == "__main__":
    unittest.main()
