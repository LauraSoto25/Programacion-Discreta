"""
Pruebas unitarias para el Ejercicio 2 (RSA de juguete).
Ejecutar con: python -m unittest discover -s tests
"""

import unittest
import sys
import os

# Asegurar que el directorio raíz del repositorio (que contiene 'src') esté en sys.path
directorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if directorio_raiz not in sys.path:
    sys.path.insert(0, directorio_raiz)

from src.cripto.rsa import euclides_extendido, inverso_modular, generar_llaves, cifrar, descifrar

class TestRSA(unittest.TestCase):

    def test_caso_minimo_obligatorio(self):
        """Caso de prueba obligatorio según enunciado"""
        p = 61
        q = 53
        e = 17
        M = 65
        
        n = p * q
        phi = (p - 1) * (q - 1)
        d = inverso_modular(e, phi)
        
        self.assertEqual(n, 3233)
        self.assertEqual(phi, 3120)
        self.assertEqual(d, 2753)
        
        C = cifrar(M, e, n)
        self.assertEqual(C, 2790)
        
        M_recuperado = descifrar(C, d, n)
        self.assertEqual(M_recuperado, 65)

    def test_euclides_extendido(self):
        """Verifica que el algoritmo de Euclides Extendido funciona correctamente."""
        # gcd(30, 20) = 10, 30(1) + 20(-1) = 10
        gcd, x, y = euclides_extendido(30, 20)
        self.assertEqual(gcd, 10)
        self.assertEqual(30 * x + 20 * y, 10)
        
        # gcd(17, 3120) = 1
        gcd, x, y = euclides_extendido(17, 3120)
        self.assertEqual(gcd, 1)
        self.assertEqual(17 * x + 3120 * y, 1)

    def test_exponente_invalido(self):
        """Debe lanzar ValueError si e no es coprimo con phi(n)."""
        # p=7, q=11 => phi(n) = 60
        # e=4 no es válido (gcd(4, 60) = 4)
        with self.assertRaises(ValueError):
            inverso_modular(4, 60)

    def test_generar_llaves(self):
        """Prueba de integración de generación de llaves."""
        publica, privada = generar_llaves(61, 53, 17)
        self.assertEqual(publica, (17, 3233))
        self.assertEqual(privada, (2753, 3233))

    def test_mensaje_grande_invalido(self):
        """El mensaje a cifrar debe ser menor que n."""
        with self.assertRaises(ValueError):
            cifrar(4000, 17, 3233)  # 4000 > 3233

if __name__ == "__main__":
    unittest.main()
