class TCPLatency:
    def __init__(self, latency=-1, link=None):
        self.latency = float(latency)
        self.link = link
        self.__alpha__ = 0.5
        
    def get_Latency(self):
        return self.latency
    
    def update_Latency(self, completion, arrival):
        l = float(completion) - float(arrival)
        if self.latency < 0:
            self.latency = l
        else:
            self.latency = (self.__alpha__ * l) + ((1 - self.__alpha__) * self.latency)
            # EWMA: L_{n+1} = \alpha l_n + (1-\alpha) L_n
#         print(self.latency)
    
    def get_Link(self):
        return self.link   
    
    def __repr__(self):
        return str(self.latency)