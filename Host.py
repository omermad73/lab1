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

    def create_l2_message(self, timeline, all_hosts, all_l2messages, min_payload_size, max_payload_size, printing_flag):

        dest_host = self.get_random_host(all_hosts)

        # Create an L2 Message
        dest_mac = dest_host.mac
        payload_size = self.get_random_payload_size(min_payload_size, max_payload_size)

        l2_message = L2Message(self.mac, dest_mac, payload_size, "data")
        all_l2messages.append(l2_message)
        self.total_tx_bytes += payload_size
        if printing_flag == 1:  # on
            time =timeline.events[0].scheduled_time
            print("Host:",l2_message.src_mac, "\033[32mcreated\033[0m an L2 Message (size:", l2_message.message_size, ")", end=' ')
            print("at time:", f"{time:.6f}")
        self.sending_l2_message(timeline, dest_host, l2_message)  # sending the message

    def sending_l2_message(self, timeline, dest_host, l2_message):
        # sending the message
        dest_id = dest_host.id
        time = timeline.events[0].scheduled_time2 + 3  # "-1" - idk how calc this shit ------------------------------------- need to be fix ---------------
        event = Event(time, "message received", self.id, dest_id, l2_message.id)
        timeline.add_event(event)

    def receiving_l2_message(self, l2_message,time, printing_flag):
        # sending the message
        self.total_tx_bytes += l2_message.message_size
        if printing_flag == 1:  # onf"\033[32m{text}\033[0m"
            print("Host:", self.mac, "\033[31mdestroyed\033[0m an L2 Message (size: ", str(l2_message.message_size), ")", "at time:", f"{time:.6f}")

    def print_statistics(self, printing_flag):
        # Print the total bytes sent and received if printing flag is ON
        if printing_flag:
            print("Host", self.mac, "sent", self.total_tx_bytes, "Bytes")
            print("Host", self.mac, "received", self.total_rx_bytes, "Bytes")

    def get_random_host(self, all_hosts):
        # Get a random index for selecting a destination host
        all_hosts.remove(self)
        random_index = random.randint(0, len(all_hosts) - 1)
        all_hosts.append(self)

        return all_hosts[random_index]

    def get_random_payload_size(self, min_payload_size, max_payload_size):
        # Generate a random payload size between the min and max payload size
        payload_size = random.randint(min_payload_size, max_payload_size)

        return payload_size