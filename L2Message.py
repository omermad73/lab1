from GNO import GNO


class L2Message(GNO):
    def __init__(self, src_mac, dst_mac, message_size, message_type):
        super().__init__("L2Message")
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.message_size = message_size
        self.message_type = message_type