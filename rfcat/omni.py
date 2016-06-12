# Omnipod Quick Setup for rfcat
#
# sudo rfcat -r 
# %run omni.py
# quick_setup(d, 40650, 1)

from rflib import *
import sys
import binascii

def packet_valid(p):
	"""packet_valid is a basic sanity check"""
	if ord(p[0]) == 0xe0:
		return True
	return False

def flip_bytes(data):
	"""flip_bytes inverts bytes from rfcat IEEE manchester to non-IEEE manchester or back"""
	bytes = map(lambda x: ord(x) ^ 0xff, data.decode("hex"))
	return binascii.hexlify(bytearray(bytes))

def quick_setup(device, bitrate, check=False):
	"""quick_setup is used to setup rfcat to quickly decode omnipod signals"""
	print "Usage: quick_setup(rfcat_device, bitrate, check_valid=False)"
	device.setFreq(433.91e6)
	device.setMdmModulation(MOD_2FSK)
	device.setPktPQT(1)
	device.setMdmSyncMode(2)
	device.setMdmSyncWord(0x54c3)
	device.makePktFLEN(60)
	device.setEnableMdmManchester(True)
	device.setMdmDRate(bitrate)
	print "Bitrate: %s" % bitrate

	while not keystop():
		try:
			pkt,ts = device.RFrecv()
			if check == 1 and packet_valid(pkt):
				print "Received: %s" % flip_bytes(pkt.encode('hex'))
			elif check == 0:
				try: 
					print "Received: %s" % flip_bytes(pkt.encode('hex'))
				except:
					pass
		except ChipconUsbTimeoutException:
			pass

	sys.stdin.read(1)