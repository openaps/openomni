import unittest
from message import Message
from commands import *

class MessageTestCase(unittest.TestCase):

    def test_data_for_crc(self):
        msg = Message("1f01482a", 5, 0x10, "0e0100".decode('hex'))
        self.assertEqual(msg.data_for_crc(), "1f01482a10030e0100".decode('hex'))

    def test_data_for_longer_crc(self):
        body = "1a0e3f63a4f90100d3013840012c012c160e7c000bb8000927c00bb8000927c0".decode('hex')
        msg = Message("1f07b1ee", 14, 0x18, body)
        self.assertEqual(len(msg.data_for_crc()), 38)

    def test_crc(self):
        msg = Message("1f01482a", 5, 0x10, "0e0100".decode('hex'))
        self.assertEqual(msg.computed_crc(), 0x802c)

    def test_packet_generation(self):
        msg = Message("1f07b1ee", 8, 0x08, "0e0100".decode('hex'))
        packets = msg.packets()
        self.assertEqual(len(packets), 1)
        self.assertEqual(packets[0].raw_hex(), "1f07b1eea81f07b1ee08030e010082b3a4")

    def test_multiple_packet_message(self):
        body = "1a0eeb5701b202010a0101a000340034170d000208000186a0000000000000".decode('hex')
        msg = Message("1f07b1ee", 14, 0x18, body)
        packets = msg.packets()
        self.assertEqual(len(packets), 2)
        self.assertEqual(packets[0].raw_hex(), "1f07b1eeae1f07b1ee181f1a0eeb5701b202010a0101a000340034170d000208000186a019")
        self.assertEqual(packets[1].raw_hex(), "1f07b1ee900000000000000251e2")

        #1f07b1ee900000000000000251e2

    def test_commands_from_message(self):

        body = "1a0e9891474a01008101384000040004".decode('hex')
        msg = Message("1f01482a", 0, 0x14, body)

        self.assertEqual(1, len(msg.commands()))

        insulin_cmd = msg.commands()[0]

        self.assertTrue(isinstance(insulin_cmd, InsulinScheduleCommand))
