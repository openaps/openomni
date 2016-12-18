import crc16

class Message(object):
    def __init__(self, pod_id, byte9, body=""):
        self.pod_id = pod_id
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
