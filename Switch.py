import copy
from L2Message import L2Message


class Switch:
    def __init__(self, num_ports, ttl=10):
        super().__init__("Switch")
        if not (num_ports & (num_ports - 1) == 0) and num_ports != 0:
            raise ValueError("Number of ports must be a power of 2.")
        self.num_ports = num_ports
        self.ports = [None] * num_ports
        self.ttl = ttl  # Time-to-live for MAC table entries
        self.mac_table = [{'used': False, 'mac': None, 'port': None, 'time': None} for _ in range(10)]

    def update_mac_table(self, mac, port, current_time):
        # Look for an existing entry to update or an empty/expired slot
        for entry in self.mac_table:
            if entry['used'] and entry['mac'] == mac:
                entry['port'] = port
                entry['time'] = current_time
                return
        for entry in self.mac_table:  # If no existing entry is found, look for an empty slot
            if not entry['used'] or current_time - entry['time'] >= self.ttl:
                entry['used'] = True
                entry['mac'] = mac
                entry['port'] = port
                entry['time'] = current_time
                return

    def find_port(self, mac, current_time):
        for entry in self.mac_table:
            if entry['used'] and entry['mac'] == mac and current_time - entry['time'] < self.ttl:
                return entry['port']
        return None

    def handle_message(self, port, l2_message, current_time):
        src_mac = l2_message.src_mac
        dst_mac = l2_message.dst_mac

        self.update_mac_table(src_mac, port, current_time)

        dest_port = self.find_port(dst_mac, current_time)
        if dest_port is not None:  # If the destination port is found in the MAC table
            if self.ports[dest_port] is not None:  # If the destination port is connected
                self.send_message(dest_port, l2_message)
            else:
                self.flood_message(port, l2_message)
        else:
            self.flood_message(port, l2_message)  # If the destination port is not found, flood the message

    def flood_message(self, incoming_port, l2_message):
        for port, link in enumerate(self.ports):
            if port != incoming_port and link is not None:
                duplicated_message = copy.copy(l2_message)
                self.send_message(port, duplicated_message)

    def send_message(self, port, l2_message):  # TODO: Implement this method
        # Send the L2 message to the given port
        # This would interact with the simulation's event system
        pass

    def connect_port(self, port, link):
        if port < 0 or port >= self.num_ports:
            raise ValueError("Invalid port number.")
        self.ports[port] = link

    def print_mac_table(self, current_time):
        print("MAC Table:")
        for entry in self.mac_table:
            if entry['used']:
                valid = "Valid" if entry['used'] and (current_time - entry['time'] < self.ttl) else "Expired"
                print(f"MAC: {entry['mac']} | Port: {entry['port']} | TTL: {entry['time']} | Status: {valid}")
