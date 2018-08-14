import unittest
from nonce import *

class NonceTestCase(unittest.TestCase):

    def test_nonces(self):
        nonces = generate_nonces(42560, 661771, 4)
        self.assertEqual(nonces[0], 0x8c61ee59)
        self.assertEqual(nonces[1], 0xc0256620)
        self.assertEqual(nonces[2], 0x15022c8a)
        self.assertEqual(nonces[3], 0xacf076ca)
