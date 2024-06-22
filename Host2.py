from Host import Host
from L2Message import L2Message


class Host2(Host):
    def __init__(self, mac, total_tx_bytes=0, total_rx_bytes=0, nic=-1, dst_rnd_set = None):
        super().__init__(mac, total_tx_bytes, total_rx_bytes, nic)
        self.dst_rnd_set = dst_rnd_set
    #
    # def create_message(self, timeline, all_hosts, all_l2messages, min_payload_size, max_payload_size, printing_flag,
    #                    link):
    #     dest_host = self.get_random_host(self.dst_rnd_set)
    #     # Create an L2 Message
    #     dest_mac = dest_host.mac
    #     payload_size = self.get_random_payload_size(min_payload_size, max_payload_size)
    #
    #     l2_message = L2Message(self.mac, dest_mac, payload_size, "data")
    #     all_l2messages.append(l2_message)
    #     self.total_tx_bytes += payload_size
    #     if printing_flag == 1:  # on
    #         time = timeline.events[0].scheduled_time
    #         print("Host:", l2_message.src_mac, "\033[32mcreated\033[0m an L2 Message (size:", l2_message.message_size,
    #               ")", end=' ')
    #         print("to host", l2_message.dst_mac, "at time:", f"{time:.6f}")
    #     self.send_message(timeline, dest_host, l2_message, link)  # sending the message*
    #
