# Packet Diagrams
![Alert](https://rawgit.com/openaps/omnidocs/master/packets/status.svg)

#### packet_type (3 bits)

 * 101 = PDM
 * 111 = POD
 * 010 = ACK
 * 100 = CON (Packet Continued)

#### Status Packet Exchange 

 * PDM (0e01) (Status Request)
 * POD (1d18) (Status Response)
 * ACK

#### Bolus Packet Exchange

 * PDM (0e01) (Status Request)
 * POD (1d18) (Status Response)
 * ACK
 * PDM (1a0e) (Bolus Request)
 * ACK
 * CON
 * POD (1d**) (Delivery Confirmation??)
 * CON
 * PDM (0e01) (Status Request)
 * POD (1d18) (Status Response)
 * ACK

#### Temp Basal Packet Exchange

 * PDM (1a0e) (Basal Change Request)
 * ACK
 * CON
 * POD (1d**) (Basal Confirmation)
 * ACK
