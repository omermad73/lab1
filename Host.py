import random

class Event:
    def __init__(self, time, event_type, sender_id, receiver_id, message_id):
        self.time = time
        self.event_type = event_type
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message_id = message_id

class L2Message:
    def __init__(self, l2_message_id, source_mac, destination_mac, payload_size, data):
        self.l2_message_id = l2_message_id
        self.source_mac = source_mac
        self.destination_mac = destination_mac
        self.payload_size = payload_size
        self.data = data

class Host:
    def __init__(self, host_id, mac, nic):
        self.time = PartA.startTime
        self.host_id = host_id
        self.mac = mac
        self.nic = nic
        self.total_tx_bytes = 0
        self.total_rx_bytes = 0

    def get_host_id(self):
        return self.host_id

    def get_mac(self):
        return self.mac

    def set_mac(self, mac):
        self.mac = mac

    def get_nic(self):
        return self.nic

    def set_nic(self, nic):
        self.nic = nic

    def get_total_tx_bytes(self):
        return self.total_tx_bytes

    def set_total_tx_bytes(self, total_tx_bytes):
        self.total_tx_bytes = total_tx_bytes

    def get_total_rx_bytes(self):
        return self.total_rx_bytes

    def set_total_rx_bytes(self, total_rx_bytes):
        self.total_rx_bytes = total_rx_bytes

    def create_l2_message(self, l2_message_id, printing_flag, all_hosts, min_payload_size, max_payload_size):
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
        event = Event(time.time() - self.time, "receive a message", self.host_id, self.host_id, l2_message.l2_message_id)

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
