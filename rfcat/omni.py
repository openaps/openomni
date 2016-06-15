# Omnipod Quick Setup for rfcat
#
# pip install crccheck
# sudo rfcat -r
# %run omni.py
# quick_setup(d, 40000, 1)

from rflib import *
import binascii
import time
import crccheck

def packet_valid(p):
	"""packet_valid is a basic sanity check"""
	if ord(p[0]) == 0xe0:
		return True
	return False

def flip_bytes(data):
	"""flip_bytes inverts bytes"""
	bytes = map(lambda x: ord(x) ^ 0xff, data.decode("hex"))
	return binascii.hexlify(bytearray(bytes))

def quick_setup(device=d, bitrate=40000, check=True):
	"""quick_setup is used to setup rfcat to quickly decode omnipod signals"""
	print "Usage: quick_setup(rfcat_device=d, bitrate=40000, check_valid=True)"
	device.setFreq(433.91e6)
	device.setMdmModulation(MOD_2FSK)
	device.setPktPQT(1)
	device.setMdmSyncMode(SYNCM_CARRIER_16_of_16)
	device.setMdmSyncWord(0x54c3)
	device.makePktFLEN(40)
	device.setEnableMdmManchester(True)
	device.setMdmDRate(bitrate)
	device.setRFRegister(0xdf18, 0x70)
	print "Bitrate: %s" % bitrate

	while not keystop():
		try:
			pkt,ts = device.RFrecv(timeout=80000)
			if check == 1 and packet_valid(pkt):

				x = 0	
				while x < len(pkt):
					packet = flip_bytes(pkt[:len(pkt) - (x + 1)].encode('hex'))
					data = bytearray.fromhex(packet)
					crc = "0x{:02x}".format(crccheck.crc.Crc8.calc(data))
					if crc == "0x" + flip_bytes(pkt[len(pkt) - (x + 1):len(pkt) - x].encode('hex')):
						packet_length = (len(packet) / 2) + 1
						print "Len: " + str(packet_length),
						print "CRC: " + crc,
						print "ID: %s" % flip_bytes(pkt[0:3].encode('hex')), 
						print "\tTYPE|SEQ: %s" % bin(int(flip_bytes(pkt[4].encode('hex')),16)),
						print "\tID2: %s" % flip_bytes(pkt[5:8].encode('hex')),
						print "\t?: %s" % flip_bytes(pkt[9].encode('hex')),
						print "\tCMD?: %s" % flip_bytes(pkt[10].encode('hex')),
						print "\t?: %s" % flip_bytes(pkt[11:packet_length].encode('hex'))
					x += 1

			elif check == 0:
				print "Received: %s" % flip_bytes(pkt.encode('hex'))

		except ChipconUsbTimeoutException:
			print "ChipconUsbTimeoutException"
			time.sleep(0.5)
			

	sys.stdin.read(1)
