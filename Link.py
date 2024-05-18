from GNO import GNO


class Link(GNO):
    def __init__(self, host1, host2, tx_rate, propagation=0.0, error_rate=0.0):
        super().__init__("Link")  #id
        self.host1 = host1
        self.host2 = host2
        self.tx_rate = tx_rate
        self.propagation = propagation
        self.error_rate = error_rate