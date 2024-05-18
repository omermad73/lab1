from GNO import GNO


class L2Message(GNO):
    def __init__(self, src_mac, dst_mac, message_size, message_type):
        super().__init__("L2Message")
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.message_size = message_size
        self.message_type = message_type

    @property
    def src_mac(self):
        return self._src_mac

    @src_mac.setter
    def src_mac(self, value):
        self._src_mac = value

    @property
    def dst_mac(self):
        return self._dst_mac

    @dst_mac.setter
    def dst_mac(self, value):
        self._dst_mac = value

    @property
    def message_size(self):
        return self._message_size

    @message_size.setter
    def message_size(self, value):
        self._message_size = value

    @property
    def message_type(self):
        return self._message_type

    @message_type.setter
    def message_type(self, value):
        self._message_type = value