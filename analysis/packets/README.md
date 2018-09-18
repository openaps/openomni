# Packet Structure
![Alert](https://rawgit.com/openaps/omnidocs/master/packets/packet.svg)

At the hardware level, the pod_address_1, packet type, sequence, and crc are stripped, and the remaining data is presented to the firmware.

#### packet_type (3 bits)

 * 101 = PDM
 * 111 = POD
 * 010 = ACK
 * 100 = CON (Packet Continued)

#### sequence (5 bits)

A counter that wraps around from 0 to 31.  Each subsequent packet, whether from PDM or pod, should have the next sequence value

#### crc

A standard 8 bit CRC

