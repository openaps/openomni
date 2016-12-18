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
        message_type = self.body[0:2]
        body_remaining = self.body[2:] + self.computed_crc_bytes()
        packets = []
        while len(body_remaining) > 0:
            packet = Packet()
            packet.pod_address_1 = self.pod_id
            packet.sequence = self.start_seq + len(packets) * 2
            if len(packets) == 0:
                packet.packet_type = Packet.PACKET_TYPE_PDM
                packet.pod_address_2 = self.pod_id
                packet.byte9 = self.byte9
                packet.message_type = message_type
                segment_len = min(Packet.MAX_BODY_SEGMENT_LEN,len(body_remaining))
                packet.body = body_remaining[:segment_len]
                packet.body_len = len(self.body)
                body_remaining = body_remaining[segment_len:]
            else:
                packet.packet_type = Packet.PACKET_TYPE_CON
                segment_len = min(Packet.MAX_CON_BODY_SEGMENT_LEN,len(body_remaining))
                packet.body = body_remaining[:segment_len]
                body_remaining = body_remaining[segment_len:]

            packets.append(packet)

        return packets

        #1f07b1ee9000000000000002510251f3
        #1f07b1ee900000000000000251e2
