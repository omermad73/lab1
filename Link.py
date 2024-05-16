class Link:
    def __init__(self, host1, host2, tx_rate):
        self.host1 = host1
        self.host2 = host2
        self.tx_rate = tx_rate
        self.propagation = 0.0
        self.error_rate = 0.0

    def get_host1(self):
        return self.host1

    def set_host1(self, host1):
        self.host1 = host1

    def get_host2(self):
        return self.host2

    def set_host2(self, host2):
        self.host2 = host2

    def get_tx_rate(self):
        return self.tx_rate

    def set_tx_rate(self, tx_rate):
        self.tx_rate = tx_rate

    def get_propagation(self):
        return self.propagation

    def set_propagation(self, propagation):
        self.propagation = propagation

    def get_error_rate(self):
        return self.error_rate

    def set_error_rate(self, error_rate):
        self.error_rate = error_rate
```

This Python code mirrors the structure and functionality of the provided Java class `Link`.
