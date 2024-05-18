import random
from GNO import GNO
from Event import Event
from L2Message import L2Message
from Timeline import Timeline


class Host(GNO):
    def __init__(self, mac, total_tx_bytes=0, total_rx_bytes=0, nic=-1):
        super().__init__("Host")
        self.mac = mac
        self.nic = nic  # if nic = -1 the host doesn't connect to any link
        self.total_tx_bytes = total_tx_bytes
        self.total_rx_bytes = total_rx_bytes

    def create_l2_message(self, timeline, all_hosts, min_payload_size, max_payload_size, printing_flag):

        dest_host = self.get_random_host(all_hosts)

        # Create an L2 Message
        dest_mac = dest_host.mac
        payload_size = self.get_random_payload_size(min_payload_size, max_payload_size)

        l2_message = L2Message(self.mac, dest_mac, payload_size, "data")
        self.total_tx_bytes += payload_size
        if printing_flag == 1:  # on
            print("Host: " + str(l2_message.src_mac) + " created an L2 Message (size: " + str(l2_message.message_size) + ")")
        self.sending_l2_messgae(timeline, dest_host, l2_message)  # sending the message

    def sending_l2_messgae(self, timeline, dest_host, l2_message):
        # sending the message
        dest_id = dest_host.id
        time = 1  # "-1" - idk how calc this shit ------------------------------------- need to be fix ---------------
        event = Event(time, "Send message", self.id, dest_id, l2_message.id)
        timeline.add_event(event)

    def print_statistics(self, printing_flag):
        # Print the total bytes sent and received if printing flag is ON
        if printing_flag:
            print("Host", self.mac, "sent", self.total_tx_bytes, "Bytes")
            print("Host", self.mac, "received", self.total_rx_bytes, "Bytes")

    def get_random_host(self, all_hosts):
        # Get a random index for selecting a destination host
        random_index = random.randint(0, len(all_hosts) - 1)

        return all_hosts[random_index]

    def get_random_payload_size(self, min_payload_size, max_payload_size):
        # Generate a random payload size between the min and max payload size
        payload_size = random.randint(min_payload_size, max_payload_size)

        return payload_size