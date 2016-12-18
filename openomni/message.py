import crc16
from packet import Packet

class Message(object):
    def __init__(self, pod_id, start_seq, byte9, body=""):
        self.pod_id = pod_id
        self.start_seq = start_seq
        self.byte9 = byte9
        self.body = body

    def data_for_crc(self):
        data = self.pod_id.decode('hex')
        data += chr(self.byte9)
        data += chr(len(self.body))
        data += self.body
        return data

    def computed_crc(self):
        return crc16.calc(self.data_for_crc())

    def computed_crc_bytes(self):
        crc = self.computed_crc()
        return chr(crc >> 8) + chr(crc & 0xff)

    def packets(self):
        if len(self.body) > 23:
            raise RuntimeError("No support for multi-packet messages yet.")

        packet = Packet()
        packet.pod_address_1 = self.pod_id
        packet.packet_type = Packet.PACKET_TYPE_PDM
        packet.sequence = self.start_seq
        packet.pod_address_2 = self.pod_id
        packet.byte9 = self.byte9
        packet.body = self.body[2:] + self.computed_crc_bytes()
        packet.body_len = len(self.body)
        packet.message_type = self.body[0:2]
        return [packet]
