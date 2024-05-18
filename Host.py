import random
from GNO import GNO
from Event import Event



class Host(GNO):
    def __init__(self, mac, nic, total_tx_bytes, total_rx_bytes):
        super().__init__("Host")
        self.mac = mac
        self.nic = nic
        self.total_tx_bytes = total_tx_bytes
        self.total_rx_bytes = total_rx_bytes

    @property
    def mac(self):
        return self._mac

    @mac.setter
    def mac(self, value):
        self._mac = value

    @property
    def nic(self):
        return self._nic

    @nic.setter
    def nic(self, value):
        self._nic = value

    @property
    def total_tx_bytes(self):
        return self._total_tx_bytes

    @total_tx_bytes.setter
    def total_tx_bytes(self, value):
        self._total_tx_bytes = value

    @property
    def total_rx_bytes(self):
        return self._total_rx_bytes

    @total_rx_bytes.setter
    def total_rx_bytes(self, value):
        self._total_rx_bytes = value

    def create_l2_message(self):

    def create_l2_message_old(self, l2_message_id, printing_flag, all_hosts, min_payload_size, max_payload_size):
        # New "create a message" event
        event = Event(time.time() - self.time, "create a message", self.host_id, self.host_id, l2_message_id)

        # Create an L2 Message
        destination_mac = self.get_random_destination_mac(all_hosts)
        payload_size = self.get_random_payload_size(min_payload_size, max_payload_size)

        l2_message = L2Message(l2_message_id, self.mac, destination_mac, payload_size, "data")

        self.total_tx_bytes += payload_size

        # Print the L2 Message creation if printing flag is ON
        if printing_flag:
            print("Host", self.mac, "created an L2 Message (size:", payload_size, "Bytes)")

        def receive_l2_message(self, printing_flag, l2_message):
        # New "receive a message" event
        event = Event(time.time() - self.time, "receive a message", self.host_id, self.host_id,
                      l2_message.l2_message_id)

        # Update the total bytes received
        self.total_rx_bytes += l2_message.payload_size

        # Print the L2 Message destruction if printing flag is ON
        if printing_flag:
            print("Host", self.mac, "destroyed an L2 Message (size:", l2_message.payload_size, "Bytes)")

        # Destroy the L2 Message
        l2_message = None

    def print_statistics(self, printing_flag):
        # Print the total bytes sent and received if printing flag is ON
        if printing_flag:
            print("Host", self.mac, "sent", self.total_tx_bytes, "Bytes")
            print("Host", self.mac, "received", self.total_rx_bytes, "Bytes")

    def get_random_destination_mac(self, all_hosts):
        # Get a random index for selecting a destination host
        random_index = random.randint(0, len(all_hosts) - 1)

        # Get the MAC address of the destination host
        destination_mac = all_hosts[random_index].get_mac()

        return destination_mac

    def get_random_payload_size(self, min_payload_size, max_payload_size):
        # Generate a random payload size between the min and max payload size
        payload_size = random.randint(min_payload_size, max_payload_size)

        return payload_size