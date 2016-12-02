import numpy as np
import pandas as pd
import itertools
import dateutil
from openomni.packet import Packet
from diff_message import DiffMessage


# Takes an array of bits, like [0,1,0,0,1,0,0,0,0,1,0,0],
# And returns a hex string: '4840'
# The result is padded to full bytes by inserting zero bits at the end.
def packbits_hex(bits):
    return "".join(map(lambda x: chr(x).encode('hex'), np.packbits(bits)))

# Takes a hex string, like 'a82b3c'
# And returns a numpy array of bits: [1 0 1 0 1 0 0 0 0 0 1 0 1 0 1 1 0 0 1 1 1 1 0 0]
def hex_unpackbits(hexstr):
    return np.unpackbits(np.frombuffer(hexstr.decode('hex'), dtype=np.uint8))

def parse_packet_file(filename):
    lines = open(filename, "rt").readlines()
    return map(lambda x: Packet().assign_from_string(x), lines)

def packets_to_pandas(packets):
    return pd.DataFrame(packets).set_index('received_at')

# This expresses our theory about which bits are message hash, and which bits
# are included in message hash calculation. Takes a full message and splits it
# into (message,hash)
def message_hash_split(data):
    # Everything except ID1, byte 4 (sequence & flags), packet crc, and 16bit chksum
    msg = data[5:-3]
    chksum = data[-3:-1]
    return (msg, chksum)

# Builds a dictionary that maps bitwise observed changes in messages to
# bitwise changes in message hash
def build_bitdiff_dictionary(packets):
    unique_packet_data = set([p.tx_data() for p in packets])
    data = [message_hash_split(d) for d in unique_packet_data]

    cracked_bits_dict = {}
    for c in itertools.combinations(data, 2):
        d = DiffMessage(c)
        if d.diff_bits_count == 0:
            continue
        if d.diff_bits_key not in cracked_bits_dict:
            cracked_bits_dict[d.diff_bits_key] = d.dc
    return cracked_bits_dict
