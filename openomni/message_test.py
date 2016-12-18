import unittest
from message import Message

class MessageTestCase(unittest.TestCase):

    def test_data_for_crc(self):
        msg = Message("1f01482a", 0x10, "0e0100".decode('hex'))
        self.assertEqual(msg.data_for_crc(), "1f01482a10030e0100".decode('hex'))

    def test_crc(self):
        msg = Message("1f01482a", 0x10, "0e0100".decode('hex'))
        self.assertEqual(msg.computed_crc(), 0x802c)
