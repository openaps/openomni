#!/usr/bin/env python

from openomni.message import Message
from openomni.nonce import generate_nonces
import sys
import struct

def main(argv):

    if len(argv) != 4:
        # ./openomni/bin/bolus.py 42539 310475 7dc0c970 0.1
        print "Usage: bolus.py lot_id tid last_nonce amount"
        exit(-1)

    print("argv = %s" % argv)

    (lot_id, tid, last_nonce, amount) = argv

    lot_id = int(lot_id)
    tid = int(tid)
    last_nonce = int(last_nonce, 16)

    print "lot_id = %08x" % lot_id
    print "tid = %08x" % tid
    print "last_nonce = %08x" % last_nonce

    nonces = generate_nonces(lot_id, tid, 10240)
    last_nonce_idx = nonces.index(last_nonce)
    print "last_nonce_idx = %d" % last_nonce_idx

    # print("Nonces = %s", nonces)
    # for nonce in nonces:
    #     print "Nonce: %08x" % nonce

    nonce = nonces[last_nonce_idx + 1]
    print "Next nonce = %08x" % nonce

    #1a0e 03117123 02 002501002000020002170d40001400030d40 000000000000 01cb 0.10U

    # Hardcode 0.1U bolus
    print "Bolus: 1a0e" + ("%08x" % nonce) + "02002501002000020002170d40001400030d40000000000000"

if __name__ == "__main__":
    main(sys.argv[1:])
