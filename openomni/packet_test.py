import unittest
from packet import Packet

class PacketTestCase(unittest.TestCase):

    def test_long_body(self):
        packet = Packet("1f07b1eeae1f07b1ee181f1a0eeb5701b202010a0101a000340034170d000208000186a019".decode('hex'))
        self.assertTrue(packet.is_valid())
        self.assertEqual(packet.body_len, 31)
        self.assertEqual(packet.packet_type, Packet.PACKET_TYPE_PDM)

    def test_ack_packet(self):
        packet = Packet("1f07b1ee4f1f07b1eeef".decode('hex'))
        self.assertTrue(packet.is_valid())
        self.assertEqual(packet.packet_type, Packet.PACKET_TYPE_ACK)

    def test_con_packet(self):
        packet = Packet("1f07b1ee900000000000000251e2".decode('hex'))
        self.assertTrue(packet.is_valid())
        self.assertEqual(packet.packet_type, Packet.PACKET_TYPE_CON)

    def test_init_pdm_packet_with_extraneous_data(self):
        packet = Packet("1f07b1eeae1f07b1ee181f1a0eeb5701b202010a0101a000340034170d000208000186a01912345678".decode('hex'))
        self.assertTrue(packet.is_valid())
        self.assertEqual(packet.packet_type, Packet.PACKET_TYPE_PDM)

    def test_init_ack_packet_with_extraneous_data(self):
        packet = Packet("1f01482a5e1f01482ae51824c9e2fa95146a9a9444bbfa0f1474514e7d".decode('hex'))
        self.assertTrue(packet.is_valid())
        self.assertEqual(packet.packet_type, Packet.PACKET_TYPE_ACK)
