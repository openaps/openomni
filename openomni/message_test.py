import unittest
from message import Message

class MessageTestCase(unittest.TestCase):

    def test_data_for_crc(self):
        msg = Message("1f01482a", 5, 0x10, "0e0100".decode('hex'))
        self.assertEqual(msg.data_for_crc(), "1f01482a10030e0100".decode('hex'))

    def test_crc(self):
        msg = Message("1f01482a", 5, 0x10, "0e0100".decode('hex'))
        self.assertEqual(msg.computed_crc(), 0x802c)

    def test_packet_generation(self):
        msg = Message("1f07b1ee", 8, 0x08, "0e0100".decode('hex'))
        packets = msg.packets()
        self.assertEqual(len(packets), 1)
        self.assertEqual(packets[0].raw_hex(), "1f07b1eea81f07b1ee08030e010082b3a4")
