from PcktTypes import PcktTypes
from Servers import Servers
from TCPflow import TCPflow
from TCPlatency import TCPLatency



class IPList:
    def __init__(self):
        self.servers = Servers()
        self.IP = dict() #2^24
        self.p0 = self.p1 = self.p2 = self.p3 = self.p4 = 0
        self.serverTimeOut = 1
        self.pcktCount = 0
        
        
        
    def add(self, packet, currentTime, detectionDelay):
        tokens = packet.split(',')
        tokens[6] = ','.join(str for str in tokens[6:])
        if tokens[6].find('>') < 0: #no port = not TPC packet, skip
            return True
        srcIP = tokens[2][1:-1]
        destIP = tokens[3][1:-1]
        srcPort = tokens[6].split('>')[0].strip()[1:]
        destPort = tokens[6].split('>')[1].strip().split(' ')[0]
        arrivalTime = float(tokens[1][1:-1])
        if(arrivalTime > currentTime+detectionDelay):
            return False
#         self.pcktCount += 1
        prefix = '.'.join(str for str in srcIP.split('.')[0:3])
        suffix = srcIP.split('.')[3]    
        if tokens[6].find('[SYN]') >= 0:
            #add to the list
            if prefix in self.IP:
                #search for src socket
                for flow in self.IP[prefix][1:]:
                    if flow.srcIPsuffix == suffix and flow.srcPort == srcPort:
                        #update the flow (overwrite)
                        flow.flags = PcktTypes.SYN
                        flow.arrivalTime = arrivalTime
                        break
                else:
                    flow = TCPflow(suffix, srcPort, arrivalTime, PcktTypes.SYN)
                    self.IP[prefix].append(flow)
            else:   #create a header and enter the flow
                header = TCPLatency()
                flow = TCPflow(suffix, srcPort, arrivalTime, PcktTypes.SYN)
                self.IP[prefix] = [header, flow]
        elif tokens[6].find('[ACK]') >= 0:
            #search for handshake
            if prefix in self.IP:
                for flow in self.IP[prefix][1:]:
                    if flow.srcIPsuffix == suffix and flow.srcPort == srcPort:
                        self.IP[prefix][0].update_Latency(arrivalTime, flow.arrivalTime)
                        #update the flow (overwrite)
                        flow.flags |= PcktTypes.ACK
                        flow.arrivalTime = arrivalTime
        elif tokens[6].find('[SYN, ACK]') >= 0:
            #find the handshake (entry is in reverse direction)
            prefix = '.'.join(str for str in destIP.split('.')[0:3])
            suffix = destIP.split('.')[3]    
            if prefix in self.IP:
                for flow in self.IP[prefix][1:]:
                    if flow.srcIPsuffix == suffix and flow.srcPort == destPort:
                        flow.flags = flow.flags | PcktTypes.SYN_ACK
        elif tokens[6].find('RST') >= 0: ###########################
            if srcIP in self.servers.serverIPs:
                prefix = '.'.join(str for str in destIP.split('.')[0:3])
                suffix = destIP.split('.')[3]    
                if prefix in self.IP:
                    for flow in self.IP[prefix][1:]:
                        if flow.srcIPsuffix == suffix and flow.srcPort == destPort:
                            flow.flags |= PcktTypes.RST_s2c
            else:
                if prefix in self.IP:
                    for flow in self.IP[prefix][1:]:
                        if flow.srcIPsuffix == suffix and flow.srcPort == srcPort:
                            flow.flags |= PcktTypes.RST_c2s
        return True
        
    def remove(self, currentTime):
        self.p0 = self.p1 = self.p2 = self.p3 = self.p4 = 0
        self.pcktCount = 0
        sockets = []
        for prefix, row in self.IP.items():
            for flow in row[1:]:
                socket = prefix+'.'+flow.srcIPsuffix+':'+flow.srcPort
                self.pcktCount += 1
                if flow.flags == PcktTypes.RST_c2s: #usual (only RST_c2s)
                    row.remove(flow)
#                     sockets.append(socket)
                    self.p0 += 1
                elif flow.flags & PcktTypes.ACK != 0: #usual SYN & ACK => SYN_ACK
                    row.remove(flow)
#                     sockets.append(socket)
                    self.p0 += 1
                elif flow.flags == PcktTypes.RST_s2c: #unusual
                    self.p2 += 1
                    row.remove(flow)
                    sockets.append(socket)
                elif flow.flags & PcktTypes.RST_c2s != 0: #unusual (since 1st condition failed we must have SYN_ACK)
                    self.p4 += 1
                    row.remove(flow)
                    sockets.append(socket)
                elif flow.flags == PcktTypes.SYN_ACK: #potential unusual due to timeout
                    if row[0].get_Latency() < 0:
                        time = flow.arrivalTime + self.serverTimeOut
                    else:
                        time = flow.arrivalTime + row[0].get_Latency()
                    if time < currentTime:
                        self.p3 += 1
                        row.remove(flow)
                        sockets.append(socket)
                elif flow.flags == PcktTypes.SYN: #potential unusual due to timeout
                    #self.p1 += 1
                    if row[0].get_Latency() < 0:
                        time = flow.arrivalTime + self.serverTimeOut
                    else:
                        time = flow.arrivalTime + row[0].get_Latency()
                    if time < currentTime:
                        self.p1 += 1
                        row.remove(flow)
                        sockets.append(socket)
            return sockets   
        print(self.p0, self.p1, self.p2, self.p3, self.p4, end='\n')
        
        
    def __repr__(self):
        return self.IP.__str__()