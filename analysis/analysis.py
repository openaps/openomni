import numpy as np
import pandas as pd
import dateutil
from openomni.packet import Packet

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

def reassemble(df):
    # (re)assemble raw packet data
    ptype_values = {
        'PDM': 0b101,
        'POD': 0b111,
        'ACK': 0b010,
        'CON': 0b100,
        }

    blen_hex = df["BLEN"].map(lambda x: chr(int(x)).encode('hex'))
    ptype_val = df["PTYPE"].map(lambda x: ptype_values[x] << 5)
    seq_val = df["SEQ"].map(lambda x: int(x))
    b5_hex = (ptype_val + seq_val).map(lambda x: chr(x).encode('hex'))
    crc_hex = df["CRC"].map(lambda x: x.rstrip())
    header_hex_data = df["ID1"] + b5_hex
    raw_hex_data = df["ID2"] + df["B9"] + blen_hex + df["MTYPE"] + df["BODY"]
    return header_hex_data + raw_hex_data + crc_hex
