from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

import json
import crccheck
import dateutil.parser
from datetime import datetime


# Serializer for datetime
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")


class Packet(object):

    PACKET_TYPE_PDM = 0b101
    PACKET_TYPE_POD = 0b111
    PACKET_TYPE_ACK = 0b010
    PACKET_TYPE_CON = 0b100

    MAX_BODY_SEGMENT_LEN = 23
    MAX_CON_BODY_SEGMENT_LEN = 30

    PACKET_TYPE_STRINGS = {
        PACKET_TYPE_PDM: "PDM",
        PACKET_TYPE_POD: "POD",
        PACKET_TYPE_ACK: "ACK",
        PACKET_TYPE_CON: "CON",
    }
    PACKET_TYPES = dict(map(lambda x: [x[1],x[0]],PACKET_TYPE_STRINGS.items()))

    def __init__(self, data=""):
        self.received_at = None
        self.packet_type = None
        self.body = None
        self.body_len = None
        self.message_type = None
        self.crc = None
        if len(data) < 10:
            return
        self.body = None
        self.pod_address_1 = data[0:4].encode("hex")
        byte5 = ord(data[4])

        self.packet_type = byte5 >> 5

        self.sequence = byte5 & 0b11111

        if self.packet_type != Packet.PACKET_TYPE_CON:
            self.pod_address_2 = data[5:9].encode("hex")

        if (self.packet_type != Packet.PACKET_TYPE_CON and
           self.packet_type != Packet.PACKET_TYPE_ACK and len(data) > 13):
            self.byte9 = ord(data[9])
            self.body_len = ord(data[10])
            self.message_type = data[11:13]
            segment_len = min(Packet.MAX_BODY_SEGMENT_LEN,self.body_len,len(data)-14)
            self.body = data[13:(13+segment_len)]
            self.crc = ord(data[13+segment_len])
        else:
            self.byte9 = None
            self.body_len = 0
            self.message_type = None
            self.body = None
            self.crc = ord(data[9])

        if self.packet_type == Packet.PACKET_TYPE_CON:
            self.body = data[5:-1]
            self.crc = ord(data[-1])

    @staticmethod
    def from_hex(hex_str):
        return Packet(hex_str.decode("hex"))

    @staticmethod
    def flip_bytes(data):
        """flip_bytes inverts bytes"""
        bytes = map(lambda x: ord(x) ^ 0xff, data)
        return bytearray(bytes).__str__()

    def packet_type_str(self):
        if self.packet_type in Packet.PACKET_TYPE_STRINGS:
            return Packet.PACKET_TYPE_STRINGS.get(self.packet_type)
        else:
            return format(self.packet_type, '#05b')[2:]

    def assign_from_string(self, line):
        try:
            elems = line.split(' ')
            self.pod_address_2 = None
            self.byte9 = None
            self.received_at = dateutil.parser.parse(elems[0])
            for elem in elems[1:]:
                (key,v) = elem.split(':')
                if key == "ID1":
                    self.pod_address_1 = v
                if key == "ID2":
                    self.pod_address_2 = v
                if key == "PTYPE":
                    self.packet_type = self.PACKET_TYPES.get(v)
                if key == "SEQ":
                    self.sequence = int(v)
                if key == "ID2":
                    self.pod_address_2 = v
                if key == "CRC":
                    self.crc = int(v,16)
                if key == "CON":
                    self.body = v.decode('hex')
                if key == "B9":
                    self.byte9 = int(v,16)
                if key == "BLEN":
                    self.body_len = int(v)
                if key == "MTYPE":
                    self.message_type = v.decode('hex')
                if key == "BODY":
                    self.body = v.decode('hex')
        except ValueError:
            self.body = None
        except OverflowError:
            self.body = None

        return self


    def tx_data(self):
        data = self.pod_address_1.decode('hex')
        data += chr((self.packet_type << 5) + self.sequence)
        if self.packet_type == self.PACKET_TYPE_CON:
            data += self.body
        else:
            data += self.pod_address_2.decode('hex')
        if self.packet_type != self.PACKET_TYPE_CON and self.body is not None:
            data += chr(self.byte9)
            data += chr(self.body_len)
            data += self.message_type
            data += self.body
        data += chr(self.compute_crc_for(bytearray(data)))
        return data

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        if self.pod_address_1 != other.pod_address_1:
            return False
        if self.pod_address_2 != other.pod_address_2:
            return False
        if self.packet_type != other.packet_type:
            return False
        if self.message_type != other.message_type:
            return False
        if self.body != other.body:
            return False
        if self.byte9 != other.byte9:
            return False
        if self.sequence != other.sequence:
            return False
        # that'll do, pig
        return True

    def __hash__(self):
        return sum([
            hash(self.pod_address_1),
            hash(self.pod_address_2),
            hash(self.packet_type),
            hash(self.message_type),
            hash(self.body),
            hash(self.byte9),
            hash(self.sequence)])

    def __str__(self):
        if not self.is_valid():
            return "Invalid Packet"

        if self.received_at is not None:
            base_str = self.received_at.isoformat() + " "
        else:
            base_str = ""

        base_str += "ID1:%s PTYPE:%s SEQ:%02d" % (
                self.pod_address_1,
                self.packet_type_str(),
                self.sequence,
            )

        crc = self.crc or self.computed_crc()

        if self.packet_type == Packet.PACKET_TYPE_ACK:
            return "%s ID2:%s CRC:%02x" % (
                base_str,
                self.pod_address_2,
                crc,
            )
        if self.packet_type == Packet.PACKET_TYPE_CON:
            return "%s CON:%s CRC:%02x" % (
                base_str,
                self.body.encode('hex'),
                crc,
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
                crc,
            )
        else:
            # All other packets without body
            return "%s ID2:%s CRC:%02x" % (
                base_str,
                self.pod_address_2,
                self.crc,
            )

    def raw_hex(self):
        return self.tx_data().encode('hex')

    def as_dict(self):
        if self.is_valid():
            obj = {
                "pod_address_1": self.pod_address_1,
                "packet_type": self.packet_type,
                "packet_type_str": self.packet_type_str(),
                "sequence": self.sequence,
                "pod_address_2": self.pod_address_2,
                "crc": self.crc,
                "raw_packet": self.raw_hex(),
            }
            if self.byte9 is not None:
                obj["byte9"] = self.byte9
            if self.body is not None:
                obj["body"] = self.body.encode('hex')
                obj["body_len"] = self.body_len
            if self.message_type is not None:
                obj["message_type"] = self.message_type.encode('hex')
            if self.received_at is not None:
                obj["received_at"] = self.received_at
        else:
            obj = {}
        return obj

    def as_json(self):
        return json.dumps(self.as_dict(), default=json_serial, sort_keys=True, indent=4, separators=(',', ': '))

    def is_valid(self):
        if self.packet_type is None:
            return False
        if self.packet_type == self.PACKET_TYPE_CON:
            body_ok = len(self.body) >= 1
        elif self.packet_type == self.PACKET_TYPE_ACK:
            body_ok = True
        else:
            if self.body is None:
                return False
            big_body_ok = self.body_len > Packet.MAX_BODY_SEGMENT_LEN and len(self.body) == Packet.MAX_BODY_SEGMENT_LEN
            small_body_ok = self.body_len == 0 or self.body_len == len(self.body)
            body_ok = (big_body_ok or small_body_ok)
        return self.crc_ok() and body_ok

    def compute_crc_for(self, data):
        return crccheck.crc.Crc8.calc(data)

    def computed_crc(self):
        return self.compute_crc_for(bytearray(self.tx_data()[:-1]))

    def crc_ok(self):
        return self.crc == None or self.crc == self.computed_crc()
