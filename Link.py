from GNO import GNO
from Host import Host

class Link(GNO):
    def __init__(self, host1, host2, tx_rate=3, propagation=0.0, error_rate=0.0):
        super().__init__("Link")  #id
        self.host1 = host1
        self.host2 = host2
        host1.nic = self.id
        host2.nic = self.id
        self.tx_rate = tx_rate
        self.propagation = propagation
        self.error_rate = error_rate