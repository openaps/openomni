import json
import crccheck

class Packet:
    def __init__(self, data):
        self.data = data
        self.body = None
        if len(data) < 10:
            return
        self.length = format(len(data),'02')
	self.pod_address_1 = data[0:4].encode("hex")
        byte5 = ord(data[4])
        self.packet_type = byte5 >> 5
        self.sequence = format((byte5 & 0b11111), '02')
        self.pod_address_2 = data[5:9].encode("hex")
        self.message_type = None
        if len(data) > 10:
            self.body_len = ord(data[9]) 
            self.message_type = ord(data[10])
            self.body = data[11:-1]
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
        if self.body == None:
            return "L:%s ID1:%s PTYPE:%s SEQ:%s ID2:%s CRC:%02x" % (
                self.length,
		self.pod_address_1,
                format(self.packet_type, '#05b')[2:],
                self.sequence,
                self.pod_address_2,
                self.crc
            )
        else:
            return "L:%s ID1:%s PTYPE:%s SEQ:%s ID2:%s BLEN:%s MTYPE:%02x BODY:%s CRC:%02x" % (
                self.length,
		self.pod_address_1,
                format(self.packet_type, '#05b')[2:],
                self.sequence,
                self.pod_address_2,
                self.body_len,
                self.message_type,
                self.body.encode('hex'),
                self.crc
            )

    def as_json(self):
        obj = {
            "pod_address_1": self.pod_address_1,
            "packet_type": self.packet_type,
            "sequence": self.sequence,
            "pod_address_2": self.pod_address_2,
            "body_len": self.body_len,
            "message_type": self.message_type,
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
