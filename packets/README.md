# Packet Diagrams
## Status
![Alert](https://rawgit.com/openaps/omnidocs/master/packets/status.svg)

#### packet_type (3 bits)

 * 101 = PDM
 * 111 = POD
 * 010 = ACK
 * 100 = ?? body length (3,6) (seen from PDM)

#### message_type

 * 0x03 - get status
 * 0x0a - get status response
