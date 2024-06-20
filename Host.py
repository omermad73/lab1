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

    def create_message(self, timeline, all_hosts, all_l2messages, min_payload_size, max_payload_size, printing_flag, link):
        dest_host = self.get_random_host(all_hosts)
        # Create an L2 Message
        dest_mac = dest_host.mac
        payload_size = self.get_random_payload_size(min_payload_size, max_payload_size)

        l2_message = L2Message(self.mac, dest_mac, payload_size, "data")
        all_l2messages.append(l2_message)
        self.total_tx_bytes += payload_size
        if printing_flag == 1:  # on
            time = timeline.events[0].scheduled_time
            print("Host:", l2_message.src_mac, "\033[32mcreated\033[0m an L2 Message (size:", l2_message.message_size,
                  ")", end=' ')
            print("to host", l2_message.dst_mac, "at time:", f"{time:.6f}")
        self.send_message(timeline, dest_host, l2_message, link)  # sending the message

    def send_message(self, timeline, dest_host, l2_message, link):
        # Determine destination host ID based on the link configuration
        if link.host1.id != self.id:
            dest_id = link.host1.id
        else:
            dest_id = link.host2.id
        time = timeline.events[0].scheduled_time + link.total_delay(l2_message)  #calculation of arrival time = time of sending + propagation delay
        event = Event(time, "message received", self.id, dest_id, l2_message.id, self.nic)
        timeline.add_event(event)

    def handle_message(self, l2_message, all_l2messages, timeline, current_time, port, printing_flag):
        if self.mac == l2_message.src_mac:
            raise ValueError(f"host {self.mac} received a message (size: {l2_message.message_size}) from itself")
        if l2_message.dst_mac == self.mac:
            self.total_rx_bytes += l2_message.message_payload
            if printing_flag == 1:
                print("Host:", self.mac, "\033[31mreceived\033[0m an L2 Message (size: ", str(l2_message.message_size),
                      ")", f"from {l2_message.src_mac} at time:", f"{current_time:.6f}")
        else:
            # If the destination MAC address is not the same as the host MAC address, the message is dropped
            if printing_flag == 1:
                print("Host:", self.mac, "\033[33mdropped\033[0m an L2 Message (size: ", str(l2_message.message_size),
                      ")", f"from {l2_message.src_mac} at time:", f"{current_time:.6f}")
            return

    def print_statistics(self, printing_flag):
        # Print the total bytes sent and received if printing flag is ON
        if printing_flag:
            print("Host", self.mac, "sent", self.total_tx_bytes, "Bytes")
            print("Host", self.mac, "received", self.total_rx_bytes, "Bytes")

    def get_random_host(self, all_hosts):
        # Get a random index for selecting a destination host
        all_hosts.remove(self)
        random_index = random.randint(0, len(all_hosts) - 1)
        random_host = all_hosts[random_index]
        all_hosts.append(self)
        return random_host

    def get_random_payload_size(self, min_payload_size, max_payload_size):
        # Generate a random payload size between the min and max payload size
        payload_size = random.randint(min_payload_size, max_payload_size)
        return payload_size
