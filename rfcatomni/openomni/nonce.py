
def generate_nonces(lot, tid, count):
  a7 = [0]*21
  a7[0] = (lot & 0xFFFF) + 0x55543DC3 + (lot >> 16)
  a7[0] = a7[0] & 0xFFFFFFFF
  a7[1] = (tid & 0xFFFF) + 0xAAAAE44E + (tid >> 16)
  a7[1] = a7[1] & 0xFFFFFFFF

  def generate_entry():
    a7[0] = ((a7[0] >> 16) + (a7[0] & 0xFFFF) * 0x5D7F) & 0xFFFFFFFF
    a7[1] = ((a7[1] >> 16) + (a7[1] & 0xFFFF) * 0x8CA0) & 0xFFFFFFFF
    return (a7[1] + (a7[0] << 16)) & 0xFFFFFFFF

  for i in range(0, 16):
    a7[2 + i] = generate_entry()

  byte_F9 = (a7[0] + a7[1]) & 0xF

  nonces = []

  for i in range(count):
    nonce = a7[2 + byte_F9]
    #print "Nonce: %08x" % nonce
    a7[2 + byte_F9] = generate_entry()
    byte_F9 = nonce & 0xf
    nonces.append(nonce)

  return nonces

# for lot, tid in [[41847, 240439], [42560, 621607], [42560, 661771]]:
#   print "Lot: %d, TID: %d" % (lot, tid)
#   nonces = generate_nonces(lot, tid, 15)
#   for nonce in nonces:
#     print "Nonce: %08x" % nonce
#   print
