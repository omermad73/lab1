import random
from GNO import GNO
from Event import Event


class Host(GNO):
    def __init__(self, mac, total_tx_bytes, total_rx_bytes, nic=-1):
        super().__init__("Host")
        self.mac = mac
        self.nic = nic  # if nic = -1 the host doesn't connect to any link
        self.total_tx_bytes = total_tx_bytes
        self.total_rx_bytes = total_rx_bytes


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