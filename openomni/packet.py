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

    def __init__(self, data = ""):
        self.received_at = None
        self.data = data
        if len(data) < 10:
            return
        self.body = None
        self.pod_address_1 = data[0:4].encode("hex")
        byte5 = ord(data[4])

        self.packet_type = byte5 >> 5
        if self.packet_type in Packet.PACKET_TYPE_STRINGS:
            self.packet_type_str = Packet.PACKET_TYPE_STRINGS.get(self.packet_type)
        else:
            self.packet_type_str = format(self.packet_type, '#05b')[2:]

        self.sequence = byte5 & 0b11111
        self.pod_address_2 = data[5:9].encode("hex")
        if len(self.data) > 13 and self.packet_type != Packet.PACKET_TYPE_ACK:
            self.byte9 = ord(data[9])
            self.body_len = ord(data[10])
            self.message_type = data[11:13]
            self.body = data[13:-1]
        else:
            self.byte9 = None
            self.body_len = 0
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
    	bytes = map(lambda x: ord(x) ^ 0xff, data)
    	return bytearray(bytes).__str__()

    def tx_data(self):
        data = self.pod_address_1.decode('hex')
        data += chr((self.packet_type << 5) + self.sequence)
        data += self.pod_address_2.decode('hex')
        data += chr(self.byte9)
        data += chr(self.body_len)
        data += self.message_type
        data += self.body
        data += chr(self.compute_crc_for(bytearray(data)))
        return data

    def __str__(self):
        if not self.is_valid():
            return "Invalid Packet"

        if self.received_at is not None:
            base_str = self.received_at.isoformat() + " "
        else:
            base_str = ""

        base_str += "ID1:%s PTYPE:%s SEQ:%02s" % (
                self.pod_address_1,
                self.packet_type_str,
                self.sequence,
            )

        if self.packet_type == Packet.PACKET_TYPE_ACK:
            return "%s ID2:%s CRC:%02x" % (
                base_str,
                self.pod_address_2,
                self.crc,
            )
        if self.packet_type == Packet.PACKET_TYPE_CON:
            return "%s CON:%s CRC:%02x" % (
                base_str,
                self.body_continuation.encode('hex'),
                self.crc,
            )
        if self.body != None:
            # All other packets with enough bytes to have a body
            return "%s ID2:%s B9:%02x BLEN:%s MTYPE:%s BODY:%s CRC:%02x" % (
                base_str,
                self.pod_address_2,
                self.byte9,
                self.body_len,
                self.message_type.encode('hex'),
                self.body.encode('hex'),
                self.crc,
            )
        else:
            # All other packets without body
            return "%s ID2:%s CRC:%02x" % (
                base_str,
                self.pod_address_2,
                self.crc,
            )

    def as_json(self):
        obj = {
            "pod_address_1": self.pod_address_1,
            "packet_type": self.packet_type,
            "packet_type_str": self.packet_type_str,
            "sequence": self.sequence,
            "pod_address_2": self.pod_address_2,
            "crc": self.crc,
            "raw_packet": self.data.encode('hex'),
        }
        if self.byte9 is not None:
            obj["byte9"] = self.byte9
        if self.body is not None:
            obj["body"] = self.body.encode('hex')
            obj["body_len"] = self.body_len
        if self.message_type is not None:
            obj["message_type"] = self.message_type.encode('hex')
        if self.received_at is not None:
            obj["received_at"] = self.received_at.isoformat()
        return json.dumps(obj, sort_keys=True,indent=4, separators=(',', ': '))

    def is_valid(self):
        if self.data == None:
            return False
        if len(self.data) < 10:
            return False
        big_body_ok = self.body_len > 23 and len(self.body) == 23
        small_body_ok = self.body_len == 0 or self.body_len == len(self.body)
        return self.crc_ok() and (big_body_ok or small_body_ok)

    def compute_crc_for(self, data):
        return crccheck.crc.Crc8.calc(data)

    def crc_ok(self):
        return self.crc == self.compute_crc_for(bytearray(self.data[:-1]))
