
class UnknownCommand(object):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return "UnknownCommand(%s)" % (self.data.encode('hex'))


class InsulinScheduleCommand(object):
    def __init__(self, data):
        self.data = data
        self.nonce = self.data[0:4].encode('hex')
        self.table_num = ord(self.data[4])
        self.checksum = (ord(self.data[5]) << 8) + ord(self.data[6])
        self.duration = ord(self.data[7]) * 30
        self.field_a = self.data[8:10].encode('hex')
        self.rate = ((ord(self.data[10]) << 8) + ord(self.data[11])) * 0.1
        self.rate_schedule = self.data[12:14].encode('hex')

    def __str__(self):
        return ("InsulinScheduleCommand(nonce=%s, table_num=%d, checksum=%04x, duration=%dm, field_a=%s, rate=%fU/hr), rate_schedule=%s" % (self.nonce, self.table_num, self.checksum, self.duration, self.field_a, self.rate, self.rate_schedule))

COMMAND_TYPES = {
    0x1a: InsulinScheduleCommand
}
