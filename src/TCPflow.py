from PcktTypes import PcktTypes
class TCPflow:
    def __init__(self, srcIPsuffix, srcPort, arrivalTime, flags):
        self.srcIPsuffix = srcIPsuffix
        self.srcPort = srcPort
        self.arrivalTime = arrivalTime
        self.flags = flags
        
    def __repr__(self):
        s = self.srcIPsuffix+','+self.srcPort+','+str(self.arrivalTime)+',SYN';
        if self.flags & PcktTypes.SYN_ACK:
            s += ',SYN_ACK'
        if self.flags & PcktTypes.ACK:
            s += ',ACK'
        if self.flags & PcktTypes.RST_c2s:
            s += ',RST_c2s'
        if self.flags & PcktTypes.RST_s2c:
            s += ',RST_s2c'
        return s