import crc16
from packet import Packet, PacketType
from commands import COMMAND_TYPES, UnknownCommand


class Message(object):
    def __init__(self, pod_address, byte9, body=""):
        self.pod_address = pod_address
        self.byte9 = byte9
        self.body = body

    def data_for_crc(self):
        data = self.pod_address.decode('hex')
        data += chr(self.byte9)
        data += chr(len(self.body))
        data += self.body
        return data

    def computed_crc(self):
        return crc16.calc(self.data_for_crc())

    def computed_crc_bytes(self):
        crc = self.computed_crc()
        return chr(crc >> 8) + chr(crc & 0xff)

    def commands(self):
        cmd_idx = 0
        cmds = []
        while cmd_idx < len(self.body)-1:
            cmd_type = ord(self.body[cmd_idx])
            cmd_len = ord(self.body[cmd_idx+1])
            cmd_class = COMMAND_TYPES.get(cmd_type, UnknownCommand)
            cmds.append(cmd_class(self.body[cmd_idx+2:cmd_idx+2+cmd_len], cmd_type))
            cmd_idx += cmd_len + 2

        return cmds

    def packetize(self, start_sequence):
        body_remaining = self.body + self.computed_crc_bytes()
        packets = []
        while len(body_remaining) > 0:
            packet = Packet()
            packet.pod_address_1 = self.pod_address
            packet.sequence = start_sequence + len(packets) * 2
            if len(packets) == 0:
                packet.packet_type = PacketType.PDM
                packet.pod_address_2 = self.pod_address
                packet.byte9 = self.byte9
                segment_len = min(Packet.MAX_BODY_SEGMENT_LEN,len(body_remaining))
                packet.body = body_remaining[:segment_len]
                packet.body_len = len(self.body)
                body_remaining = body_remaining[segment_len:]
            else:
                packet.packet_type = PacketType.CON
                segment_len = min(Packet.MAX_CON_BODY_SEGMENT_LEN,len(body_remaining))
                packet.body = body_remaining[:segment_len]
                body_remaining = body_remaining[segment_len:]

            packets.append(packet)

        return packets
