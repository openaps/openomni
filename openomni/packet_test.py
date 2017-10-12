import unittest
from packet import Packet, PacketType

class PacketTestCase(unittest.TestCase):

    def test_long_body(self):
        packet = Packet("1f07b1eeae1f07b1ee181f1a0eeb5701b202010a0101a000340034170d000208000186a019".decode('hex'))
        self.assertTrue(packet.is_valid())
        self.assertEqual(packet.body_len, 31)
        self.assertEqual(packet.packet_type, PacketType.PDM)

    def test_ack_packet(self):
        packet = Packet("1f07b1ee4f1f07b1eeef".decode('hex'))
        self.assertTrue(packet.is_valid())
        self.assertEqual(packet.packet_type, PacketType.ACK)

    def test_con_packet(self):
        packet = Packet("1f07b1ee900000000000000251e2".decode('hex'))
        self.assertTrue(packet.is_valid())
        self.assertEqual(packet.packet_type, PacketType.CON)

    def test_init_short_pdm_packet_with_extraneous_data(self):
        packet = Packet("1f00ee84a91f00ee8434030e0100836eb01d10851a72f25018c55185cd5ac348260f515df4ff30ab0422c1c2c904aca172".decode('hex'))
        self.assertTrue(packet.is_valid())
        self.assertEqual(packet.packet_type, PacketType.PDM)
        self.assertEqual(packet.raw_hex(), "1f00ee84a91f00ee8434030e0100836eb0")

    def test_init_pdm_packet_with_extraneous_data(self):
        packet = Packet("1f07b1eeae1f07b1ee181f1a0eeb5701b202010a0101a000340034170d000208000186a01912345678".decode('hex'))
        self.assertTrue(packet.is_valid())
        self.assertEqual(packet.packet_type, PacketType.PDM)
        self.assertEqual(packet.raw_hex(), "1f07b1eeae1f07b1ee181f1a0eeb5701b202010a0101a000340034170d000208000186a019")

    def test_init_ack_packet_with_extraneous_data(self):
        packet = Packet("1f01482a5e1f01482ae51824c9e2fa95146a9a9444bbfa0f1474514e7d".decode('hex'))
        self.assertTrue(packet.is_valid())
        self.assertEqual(packet.packet_type, PacketType.ACK)
        self.assertEqual(packet.raw_hex(), "1f01482a5e1f01482ae5")

    def test_read_packet_output_format(self):
        packet = Packet().assign_from_string("2016-06-17T20:50:34.882742 ID1:1f014829 PTYPE:POD SEQ:14 ID2:1f014829 B9:24 BLEN:10 MTYPE:1d18 BODY:02ada800002be7ff021c CRC:40")
        self.assertTrue(packet.is_valid())
        self.assertEqual(packet.packet_type, PacketType.POD)
        self.assertEqual(packet.body_len, 10)
        self.assertEqual(len(packet.body), 12)  # Includes crc
        self.assertEqual(str(packet), "2016-06-17T20:50:34.882742 ID1:1f014829 PTYPE:POD SEQ:14 ID2:1f014829 B9:24 BLEN:10 BODY:1d1802ada800002be7ff021c CRC:40")


if __name__ == '__main__':
    unittest.main()
