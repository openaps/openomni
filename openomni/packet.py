import json
import crccheck

class Packet:

    PACKET_TYPE_PDM = 0b101
    PACKET_TYPE_POD = 0b111
    PACKET_TYPE_ACK = 0b010
    PACKET_TYPE_CON = 0b100

    PACKET_TYPE_STRINGS = {
        PACKET_TYPE_PDM: "PDM",
        PACKET_TYPE_POD: "POD",
        PACKET_TYPE_ACK: "ACK",
        PACKET_TYPE_CON: "CON",
    }

    def __init__(self, data):
        self.data = data
        if len(data) < 10:
            return
        self.body = None
        self.length = format(len(data),'02')
        self.pod_address_1 = data[0:4].encode("hex")
        byte5 = ord(data[4])

        self.packet_type = byte5 >> 5
        if self.packet_type in Packet.PACKET_TYPE_STRINGS:
            self.packet_type_str = Packet.PACKET_TYPE_STRINGS.get(self.packet_type)
        else:
            self.packet_type_str = format(self.packet_type, '#05b')[2:]

        self.sequence = format((byte5 & 0b11111), '02')
        self.pod_address_2 = data[5:9].encode("hex")
        if len(self.data) > 13 and self.packet_type != Packet.PACKET_TYPE_ACK:
            self.byte9 = ord(data[9])
            self.body_len = ord(data[10])
            self.message_type = data[11:13]
            self.body = data[13:-1]
        else:
            self.byte9 = None
            self.body_len = None
            self.message_type = None
            self.body = None

        if self.packet_type == Packet.PACKET_TYPE_CON:
            self.body_continuation = data[5:-1]
        self.crc = ord(data[-1])

    @staticmethod
    def from_hex(hex_str):
        return Packet(hex_str.decode("hex"))

    @staticmethod
    def flip_bytes(data):
    	"""flip_bytes inverts bytes"""
    	bytes = map(lambda x: ord(x) ^ 0xff, data.decode("hex"))
    	return binascii.hexlify(bytearray(bytes))

    def __str__(self):
        if not self.is_valid():
            return "Invalid Packet"

        if self.packet_type == Packet.PACKET_TYPE_ACK:
            return "ID1:%s PTYPE:%s SEQ:%s ID2:%s CRC:%02x" % (
                self.pod_address_1,
                self.packet_type_str,
                self.sequence,
                self.pod_address_2,
                self.crc,
            )
        if self.packet_type == Packet.PACKET_TYPE_CON:
            return "ID1:%s PTYPE:%s SEQ:%s CON:%s CRC:%02x" % (
                self.pod_address_1,
                self.packet_type_str,
                self.sequence,
                self.body_continuation.encode('hex'),
                self.crc,
            )
        return "ID1:%s PTYPE:%s SEQ:%s ID2:%s B9:%02x BLEN:%s MTYPE:%s BODY:%s CRC:%02x" % (
            self.pod_address_1,
            self.packet_type_str,
            self.sequence,
            self.pod_address_2,
            self.byte9,
            self.body_len,
            self.message_type.encode('hex'),
            self.body.encode('hex'),
            self.crc,
        )

    def as_json(self):
        obj = {
            "pod_address_1": self.pod_address_1,
            "packet_type": self.packet_type,
            "packet_type_str": self.packet_type_str,
            "sequence": self.sequence,
            "pod_address_2": self.pod_address_2,
            "byte9": self.byte9,
            "body_len": self.body_len,
            "message_type": self.message_type.encode('hex'),
            "body": self.body.encode('hex'),
            "crc": self.crc,
            "raw_packet": self.data.encode('hex'),
        }
        return json.dumps(obj, sort_keys=True,indent=4, separators=(',', ': '))

    def is_valid(self):
        return len(self.data) >= 10 and self.crc_ok()

    def crc_ok(self):
        computed_crc = crccheck.crc.Crc8.calc(bytearray(self.data[:-1]))
        return self.crc == computed_crc
