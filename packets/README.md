# Packet Diagrams
![Alert](https://rawgit.com/openaps/omnidocs/master/packets/status.svg)

#### packet_type (3 bits)

 * 101 = PDM
 * 111 = POD
 * 010 = ACK
 * 100 = ?? body length (3,6) (seen from PDM)

#### Status Packet Exchange 

 * PDM (0e01) (Status Request)
 * PDM (0e01) (Duplicate Packet)
 * POD (1d18) (Status Response)
 * ACK

#### Bolus Packet Exchange

 * PDM (0e01) (Status Request))
 * PDM (0e01) (Duplicate Packet)
 * POD (1d18) (Status Response)
 * ACK
 * PDM (1a0e) (Bolus Request)
 * PDM (1a0e) (Duplicate Packet)
 * PDM (1a0e) (Duplicate Packet)
 * ACK
 * 100
 * POD (1d**) (Delivery Confirmation??)
 * POD (1d**) (Duplicate Packet)
 * 100
 * PDM (0e01) (Status Request)
 * PDM (0e01) (Duplicate Packet)
 * POD (1d18) (Status Response)
 * ACK

#### Temp Basal Packet Exchange

 * PDM (1a0e) (Basal Change Request)
 * PDM (1a0e) (Duplicate Packet)
 * ACK
 * 100
 * POD (1d29) (Basal Confirmation)
 * POD (1d29) (Duplicate Packet)
 * POD (1d29) (Duplicate Packet)
 * ACK
