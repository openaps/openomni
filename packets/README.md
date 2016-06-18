# Packet Diagrams
![Alert](https://rawgit.com/openaps/omnidocs/master/packets/status.svg)

#### packet_type (3 bits)

 * 101 = PDM
 * 111 = POD
 * 010 = ACK
 * 100 = ?? body length (3,6) (seen from PDM)

#### Status Packet Exchange 

 * PDM (0e01) (Status Request)
 * POD (1d18) (Status Response)
 * ACK

#### Bolus Packet Exchange

 * PDM (0e01) (Status Request))
 * POD (1d18) (Status Response)
 * ACK
 * PDM (1a0e) (Bolus Request)
 * ACK
 * 100
 * POD (1d**) (Delivery Confirmation??)
 * 100
 * PDM (0e01) (Status Request)
 * POD (1d18) (Status Response)
 * ACK

#### Temp Basal Packet Exchange

 * PDM (1a0e) (Basal Change Request)
 * ACK
 * 100
 * POD (1d29) (Basal Confirmation)
 * ACK
