from GNO import GNO


class L2Message(GNO):
    def __init__(self, host1, host2, tx_rate,propagation=0.0, error_rate=0.0):
        super().__init__("Link")
        self.host1 = host1
        self.host2 = host2
        self.tx_rate = tx_rate
        self.propagation = propagation
        self.error_rate = error_rate

    @property
    def host1(self):
        return self._host1

    @host1.setter
    def host1(self, value):
        self._host1 = value

    @property
    def host2(self):
        return self._host2

    @host2.setter
    def host2(self, value):
        self._host2 = value

    @property
    def tx_rate(self):
        return self._tx_rate

    @tx_rate.setter
    def tx_rate(self, value):
        self._tx_rate = value

    @property
    def propagation(self):
        return self._propagation

    @propagation.setter
    def propagation(self, value):
        self._propagation = value

    @property
    def error_rate(self):
        return self._error_rate

    @error_rate.setter
    def error_rate(self, value):
        self._error_rate = value
