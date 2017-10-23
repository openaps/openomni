import unittest
import crc16

class CrcTestCase(unittest.TestCase):

    def test_crc_computation(self):
        msg = "1f01482a10030e0100".decode("hex")
        crc = crc16.calc(msg)
        self.assertEqual(crc, 0x802c)
