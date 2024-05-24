import copy
from GNO import GNO
from Event import Event


class Switch(GNO):
    def __init__(self, num_ports, log_file=None, ttl=10):
        super().__init__("Switch")
        if not (num_ports & (num_ports - 1) == 0) and num_ports != 0:
            raise ValueError("Number of ports must be a power of 2.")
        self.num_ports = num_ports
        self.ports = [None] * num_ports
        self.ttl = ttl  # Time-to-live for MAC table entries
        self.mac_table = [{'used': False, 'mac': None, 'port': None, 'time': None} for _ in range(10)]
        self.log_file = log_file
        self.update_counter = 1

    def update_mac_table(self, mac, port, current_time, printing_flag):
        # Look for an existing entry to update or an empty/expired slot
        for entry in self.mac_table:
            if entry['used'] and entry['mac'] == mac:
                entry['port'] = port
                entry['time'] = current_time
                if printing_flag == 1:
                    self.print_mac_table(current_time)
                return
        for entry in self.mac_table:  # If no existing entry is found, look for an empty slot
            if not entry['used'] or current_time - entry['time'] >= self.ttl:
                entry['used'] = True
                entry['mac'] = mac
                entry['port'] = port
                entry['time'] = current_time
                if printing_flag == 1:
                    self.print_mac_table(current_time)
                return

    def find_port(self, mac, current_time):
        for entry in self.mac_table:
            if entry['used'] and entry['mac'] == mac and current_time - entry['time'] < self.ttl:
                return entry['port']
        return None

    def link_to_port(self, link_id):  # Find the port number of the corresponding link
        for port, link in enumerate(self.ports):
            if link.id == link_id:
                return port
        return None

    def handle_message(self, l2_message, all_l2messages, timeline, current_time, link_id, printing_flag):
        src_mac = l2_message.src_mac
        dst_mac = l2_message.dst_mac
        port = self.link_to_port(link_id)

        self.update_mac_table(src_mac, port, current_time, printing_flag)
        if printing_flag == 1:
            print(f"Switch: {self.id} \033[34mreceived\033[0m a message (size: {l2_message.message_size}) from port {port} at time: {current_time:.6f}, MAC table updated")

        dest_port = self.find_port(dst_mac, current_time)
        if dest_port is not None:  # If the destination port is found in the MAC table
            if self.ports[dest_port] is not None:  # If the destination port is connected
                self.send_message(timeline, dest_port, l2_message, all_l2messages)
                if printing_flag == 1:
                    print(f"Switch: {self.id} \033[36msending\033[0m the message (size: {l2_message.message_size}) to port {dest_port} at time: {current_time:.6f}")
            else:
                self.flood_message(timeline, port, l2_message, all_l2messages)
        else:
            self.flood_message(timeline, port, l2_message, all_l2messages)  # If the destination port is not found, flood the message
            if printing_flag == 1:
                print(f"Switch: {self.id} \033[35mflooding\033[0m the message (size: {l2_message.message_size}) at time: {current_time:.6f}")

    def flood_message(self, timeline, incoming_port, l2_message, all_l2messages):
        for port, link in enumerate(self.ports):
            if port != incoming_port and link is not None:
                duplicated_message = copy.copy(l2_message)
                self.send_message(timeline, port, duplicated_message, all_l2messages)

    def send_message(self, timeline, port, l2_message, all_l2messages):
        # Send the L2 message to the given port
        link = self.ports[port]
        if link.host1.id != self.id:
            dest_id = link.host1.id
        else:
            dest_id = link.host2.id
        time = timeline.events[0].scheduled_time + link.total_delay(l2_message)  #calculation of arrival time = time of sending + propagation delay
        event = Event(time, "message received", self.id, dest_id, l2_message.id, link.id)
        all_l2messages.append(l2_message)
        timeline.add_event(event)

    def connect_port(self, port, link):
        if port < 0 or port >= self.num_ports:
            raise ValueError("Invalid port number.")
        self.ports[port] = link

    def connect_all_ports(self, links):  # Made to be called after initialization
        if len(links) < 0 or len(links) > self.num_ports:
            raise ValueError("Invalid port number.")

        self.ports = links
        self.ports += [None] * (self.num_ports - len(links))

    def print_mac_table(self, current_time):
        log_file = self.log_file
        if log_file:
            log_file.write(f"Table of switch {self.id} (update {self.update_counter}):\n")
            for entry in self.mac_table:
                if entry['used']:
                    valid = "Valid" if entry['used'] and (current_time - entry['time'] < self.ttl) else "Expired"
                    log_file.write(
                        f"MAC: {entry['mac']} | Port: {entry['port']} | TTL: {self.ttl - (current_time - entry['time'])} | Status: {valid}\n")
        else:
            print(f"Table of switch {self.id} (update {self.update_counter}):")
            for entry in self.mac_table:
                if entry['used']:
                    valid = "Valid" if entry['used'] and (current_time - entry['time'] < self.ttl) else "Expired"
                    print(f"MAC: {entry['mac']} | Port: {entry['port']} | TTL: {self.ttl - (current_time - entry['time'])} | Status: {valid}")
        self.update_counter += 1
