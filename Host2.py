from Host import Host
import random
from L2Message import L2Message


class Host2(Host):
    def __init__(self, mac,dst_rnd_set = None, seed = 42,total_tx_bytes=0, total_rx_bytes=0, nic=-1):
        super().__init__(mac, total_tx_bytes, total_rx_bytes, nic)
        self.dst_rnd_set = dst_rnd_set
        if seed is not None:
            random.seed(seed)

    def get_random_host(self):
        # Get a random index for selecting a destination host
        dest_pool = self.dst_rnd_set
        if dest_pool in self.dst_rnd_set:
            dest_pool.remove(self)

        random_index = random.randint(0, len(self.dst_rnd_set) - 1)
        random_host = dest_pool[random_index]
        return random_host

    def create_message(self, timeline, all_hosts, all_l2messages, min_payload_size, max_payload_size, printing_flag, link):
        dest_host = self.get_random_host()
        self.create_l2message(timeline, all_hosts, all_l2messages, min_payload_size, max_payload_size, printing_flag, link, dest_host)