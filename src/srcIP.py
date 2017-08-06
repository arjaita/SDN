class srcIP:
    def __init__(self, IP, arrivalTime, flag):
        self.IP = IP
        self.arrivalTime = arrivalTime
        self.flag = flag
    
    def get_IP(self):
        return self.IP
    
    def get_arrivalTime(self):
        return self.arrivalTime
    
    def get_flag(self):
        return self.flag
    
    def update_flag(self, flag):
        self.flag = flag
        
    def remove_IP(self):
        del(self)