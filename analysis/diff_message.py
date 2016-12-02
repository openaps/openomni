import numpy as np

# Takes two byte strings and xor's them
def diff(m1,m2):
    return [ord(a) ^ ord(b) for a,b in zip(m1,m2)]

class DiffMessage(object):

    # data is passed in like this: ((m1,c1),(m2,c2))
    def __init__(self, combination):
        self.m1 = combination[0][0]
        self.c1 = combination[0][1]
        self.m2 = combination[1][0]
        self.c2 = combination[1][1]

        # message diff
        self.dm = diff(self.m1, self.m2)

        # delta crc, aka xor value!
        self.dc = diff(self.c1, self.c2)
        self.dc = (self.dc[0] << 8) + self.dc[1]

        # diff stats
        diff_bits = np.unpackbits(np.array(self.dm, dtype=np.uint8))
        self.diff_bits_count = diff_bits.sum()
        bit_indexes = np.where(diff_bits)[0].tolist()
        self.diff_bits_key = ':'.join(str(x) for x in bit_indexes)

        self.confirmations = 0
        self.conflicts = 0

    def update_observation(self, other):
        if other.dc == self.dc:
            self.confirmations += 1
        else:
            self.conflicts += 1

    def __str__(self):
        return "%s: msg=%s, crc=%s" % (self.diff_bits_key, self.dm, self.dc)
