import queue
import math
import copy
from Switch import Switch
from Event import Event


class SwitchLab2(Switch):
    def __init__(self, num_ports, mac_table_size, q_type="input", is_fluid=False, schedule_alg='FIFO', log_file=None, ttl=10):
        super().__init__(num_ports, mac_table_size, log_file, ttl)
        self.q_type = q_type
        self.is_fluid = is_fluid
        self.schedule_alg = schedule_alg
        self.queues = self.configure_queues()
        self.totalHoLTime = 0
        self.queue_to_HoLTime = {}
        for i in range(num_ports):
            self.queue_to_HoLTime[i] = 0
        self.port_is_blocked = [False] * self.num_ports

    def configure_queues(self):
        if self.q_type == 'input' or self.q_type == 'output':
            return [queue.Queue() for _ in range(self.num_ports)]
        elif self.q_type == 'virtual_output':
            return [[queue.Queue() for _ in range(self.num_ports)] for _ in range(self.num_ports)]
        else:
            raise ValueError("Invalid queue type")

    def get_real_queue(self, queue_num):
        # Here we created a bijection between ordered pair and integer
        # The ordered pair is used to represent the virtual output queue
        # The integer is used to represent the input and output queues
        # This bijection is used to simplify the code
        if self.q_type == 'virtual_output':
            return [math.floor(queue_num / self.num_ports), queue_num % self.num_ports]
        else:
            return [queue_num]

    def get_fake_queue(self, queue_num):
        # Here is the inverse of the bijection
        if self.q_type == 'virtual_output':
            return queue_num[0] * self.num_ports + queue_num[1]
        else:
            return queue_num

    def enqueue(self, message, queue_num):
        if self.q_type == 'input' or self.q_type == 'output':
            self.queues[queue_num].put(message)
        elif self.q_type == 'virtual_output':
            self.queues[self.get_real_queue(queue_num)[0]][self.get_real_queue(queue_num)[1]].put(message)

    def dequeue(self, queue_num):
        # This function is used to dequeue a message from the queue
        # The function returns the first message after removing
        if self.q_type == 'input' or self.q_type == 'output':
            self.queues[queue_num].get()
            if self.queues[queue_num].empty():
                return None
            temp = self.queues[queue_num].get()
            self.queues[queue_num].put(temp)
            return temp
        elif self.q_type == 'virtual_output':
            self.queues[self.get_real_queue(queue_num)[0]][self.get_real_queue(queue_num)[1]].get()
            temp = self.queues[self.get_real_queue(queue_num)[0]][self.get_real_queue(queue_num)[1]].get()
            self.queues[self.get_real_queue(queue_num)[0]][self.get_real_queue(queue_num)[1]].put(temp)
            return temp

    def handle_message(self, l2_message, all_l2messages, timeline, current_time, link_id, printing_flag):
        src_mac = l2_message.src_mac
        dst_mac = l2_message.dst_mac
        port = self.link_to_port(link_id)

        if printing_flag == 1:
            print(f"Switch: {self.id} \033[34mreceived\033[0m a message (size: {l2_message.message_size}) from port"
                  f" {port} at time: {current_time:.6f}, MAC table updated")
            print(f"Source MAC: {src_mac} Destination MAC: {dst_mac}")
        self.update_mac_table(src_mac, port, current_time, printing_flag)

        if self.q_type == 'input':
            self.handle_message_input(l2_message, all_l2messages, timeline, current_time, link_id, printing_flag)
        elif self.q_type == 'output':
            self.handle_message_output(l2_message, all_l2messages, timeline, current_time, link_id, printing_flag)
        elif self.q_type == 'virtual_output':
            self.handle_message_virtual_output(l2_message, all_l2messages, timeline, current_time, link_id, printing_flag)

    def handle_message_input(self, l2_message, all_l2messages, timeline, current_time, link_id, printing_flag):
        src_mac = l2_message.src_mac
        dst_mac = l2_message.dst_mac
        port = self.link_to_port(link_id)
        time = timeline.events[0].scheduled_time
        self.enqueue(l2_message, port)

        if printing_flag == 1:
            print(f"Switch: {self.id} \033[34mreceived\033[0m a message (size: {l2_message.message_size}) from port"
                  f" {port} at time: {current_time:.6f}, MAC table updated")
            print(f"Source MAC: {src_mac} Destination MAC: {dst_mac}")

        dest_port = self.find_port(dst_mac, current_time)
        if dest_port is not None:  # If the destination port is found in the MAC table
            if self.ports[dest_port] is not None:  # If the destination port is connected
                if port != dest_port:  # if not the switch should drop the message
                    self.enqueue(l2_message, dest_port)
                    if not self.port_is_blocked[port]:
                        event = Event(time, "sending a message", self.id, self.id, l2_message.id, self.ports[port])
                        timeline.add_event(event)
            else:  # that if the link was disconnected
                pass
        else:
            self.duplicat(port,l2_message,time,printing_flag)  # duplicate the message for future flooding
            self.dequeue(port)
        if not self.port_is_blocked[port]:
            event = Event(time, "sending a message", self.id, self.id, l2_message.id, self.ports[0])
            timeline.add_event(event)

        dest_port = self.find_port(dst_mac, current_time)  # TODO: START SENDIN
        if dest_port is not None:  # If the destination port is found in the MAC table
            if self.ports[dest_port] is not None:  # If the destination port is connected
                if port != dest_port:  # if not the switch should drop the message
                    self.send_message(timeline, dest_port, l2_message, all_l2messages)
                    if printing_flag == 1:
                        print(
                            f"Switch: {self.id} \033[36msending\033[0m the message (size: {l2_message.message_size}) to port {dest_port} at time: {current_time:.6f}")
            else:  # that if the link was disconnected
                pass
        else:
            self.flood_message(timeline, port, l2_message,
                               all_l2messages)  # If the destination port is not found, flood the message
            if printing_flag == 1:
                print(
                    f"Switch: {self.id} \033[35mflooding\033[0m the message (size: {l2_message.message_size}) at time: {current_time:.6f}")

    def handle_message_output(self, l2_message, all_l2messages, timeline, current_time, link_id, printing_flag):
        dst_mac = l2_message.dst_mac
        port = self.link_to_port(link_id)


        dest_port = self.find_port(dst_mac, current_time)
        if dest_port is not None:  # If the destination port is found in the MAC table
            if self.ports[dest_port] is not None:  # If the destination port is connected
                if port != dest_port:  # if not the switch should drop the message
                    self.enqueue(l2_message, dest_port)
                    if self.port_is_blocked[dest_port] is False:
                        # If the port is not blocked, the switch will send the message
                        self.first_message_output(timeline, dest_port, all_l2messages, printing_flag)
            else:  # that if the link was disconnected
                pass
        else:
            if printing_flag == 1:
                print(f"Switch: {self.id} \033[35m will flood\033[0m the message (size: {l2_message.message_size}) "
                      f"at time: {current_time:.6f}")
            for out_port, link in enumerate(self.ports):
                if out_port != port and link is not None:
                    duplicated_message = copy.copy(l2_message)
                    self.enqueue(duplicated_message, out_port)
                    if self.port_is_blocked[out_port] is False:
                        # If the port is not blocked, the switch will send the message
                        self.first_message_output(timeline, out_port, all_l2messages, printing_flag)

    def handle_message_virtual_output(self, l2_message, all_l2messages, timeline, current_time, link_id, printing_flag):
        src_mac = l2_message.src_mac
        dst_mac = l2_message.dst_mac
        port = self.link_to_port(link_id)

        if printing_flag == 1:
            print(f"Switch: {self.id} \033[34mreceived\033[0m a message (size: {l2_message.message_size}) from port"
                  f" {port} at time: {current_time:.6f}, MAC table updated")
            print(f"Source MAC: {src_mac} Destination MAC: {dst_mac}")

        dest_port = self.find_port(dst_mac, current_time)
        if dest_port is not None:  # If the destination port is found in the MAC table
            if self.ports[dest_port] is not None:  # If the destination port is connected
                if port != dest_port:  # if not the switch should drop the message
                    self.enqueue(l2_message, self.get_fake_queue([port, dest_port]))
            else:  # that if the link was disconnected
                pass
        else:
            for out_port, link in enumerate(self.ports):
                if out_port != port and link is not None:
                    duplicated_message = copy.copy(l2_message)
                    self.enqueue(duplicated_message, self.get_fake_queue([port, out_port]))
            if printing_flag == 1:
                print(f"Switch: {self.id} \033[35m will flood\033[0m the message (size: {l2_message.message_size}) "
                      f"at time: {current_time:.6f}")

    def send_message_think(self, l2_message, all_l2messages, timeline, current_time, link_id, printing_flag):
        link = self.ports[port]  # TODO: fix this
        if link.host1.id != self.id:
            dest_id = link.host1.id
        else:
            dest_id = link.host2.id
        time = timeline.events[0].scheduled_time + link.total_delay(l2_message)  # calculation of arrival time = time
        # of sending + propagation delay
        event = Event(time, "message received", self.id, dest_id, l2_message.id, link.id)
        all_l2messages.append(l2_message)
        timeline.add_event(event)
        if printing_flag == 1:
            print(
                f"Switch: {self.id} \033[36msending\033[0m the message (size: {l2_message.message_size}) to "
                f"port {dest_port} at time: {current_time:.6f}")

        time = timeline.events[0].scheduled_time + link.transmit_delay(l2_message)  # calculation of arrival time
        # = time of sending
        event = Event(time, "transmitted", self.id, None, None, self.nic)
        timeline.add_event(event)

    def message_transmitted(self, timeline, queue_num, all_l2messages, printing_flag):  # TODO: add all_l2messages
        if printing_flag == 1:
            print(f"Switch: {self.id} \033[32mtransmitted\033[0m a message from queue {queue_num} at time: "
                  f"{timeline.events[0].scheduled_time:.6f}")

        if self.q_type == 'input':
            self.message_transmitted_input(timeline, queue_num, printing_flag)
        elif self.q_type == 'output':
            self.message_transmitted_output(timeline, queue_num, all_l2messages, printing_flag)
        else:
            self.message_transmitted_output(timeline, queue_num, printing_flag)

    def message_transmitted_input(self, timeline, queue_num, printing_flag):
        current_time = timeline.events[0].scheduled_time
        if printing_flag == 1:
            print(f"Switch: {self.id} \033[32mtransmitted\033[0m a message to link {link.id} at time: "
                  f"{current_time:.6f}")


        next_message = self.dequeue(queue_num)
        dst_mac = next_message.dst_mac
        source_port = queue_num
        dest_port = self.find_port(dst_mac, current_time)
        if dest_port is not None:  # If the destination port is found in the MAC table
            if self.ports[dest_port] is not None:  # If the destination port is connected
                if source_port != dest_port:  # if not the switch should drop the message
                    self.enqueue(next_message, dest_port)
            else:  # that if the link was disconnected
                pass
        else:
            for out_port, link in enumerate(self.ports):
                if out_port != source_port and link is not None:
                    duplicated_message = copy.copy(next_message)
                    self.enqueue(duplicated_message, out_port)
            if printing_flag == 1:
                print(f"Switch: {self.id} \033[35m will flood\033[0m the message (size: {next_message.message_size}"
                      f") "f"at time: {current_time:.6f}")

    def message_transmitted_output(self, timeline, queue_num, all_l2messages, printing_flag):
        current_time = timeline.events[0].scheduled_time

        self.port_is_blocked[queue_num] = False
        self.totalHoLTime += self.queue_to_HoLTime[queue_num]
        self.queue_to_HoLTime[queue_num] = 0
        next_message = self.dequeue(queue_num)
        if next_message is None:
            return

        dest_port = queue_num
        link = self.ports[queue_num]
        time = current_time + link.transmit_delay(next_message)  # calculation of arrival time
        # = time of sending
        self.port_is_blocked[queue_num] = True
        event = Event(time, "transmitted", self.id, None, None, queue_num)
        timeline.add_event(event)
        if printing_flag == 1:
            print(f"Switch: {self.id} \033[36msending\033[0m the message (size: {next_message.message_size}) to"
                  f" port {dest_port} at time: {current_time:.6f}")
        self.send_message(timeline, dest_port, next_message, all_l2messages)

    def first_message_output(self, timeline, queue_num, all_l2messages, printing_flag):
        current_time = timeline.events[0].scheduled_time

        next_message = self.queues[queue_num].get()
        self.queues[queue_num].put(next_message)

        self.port_is_blocked[queue_num] = False
        self.totalHoLTime += self.queue_to_HoLTime[queue_num]
        self.queue_to_HoLTime[queue_num] = 0
        next_message = self.queues[queue_num].get()
        self.queues[queue_num].put(next_message)
        if next_message is None:
            return

        dest_port = queue_num
        link = self.ports[queue_num]
        time = current_time + link.transmit_delay(next_message)  # calculation of arrival time
        # = time of sending
        self.port_is_blocked[queue_num] = True
        event = Event(time, "transmitted", self.id, None, None, queue_num)
        timeline.add_event(event)
        if printing_flag == 1:
            print(f"Switch: {self.id} \033[36msending\033[0m the message (size: {next_message.message_size}) to"
                  f" port {dest_port} at time: {current_time:.6f}")
        self.send_message(timeline, dest_port, next_message, all_l2messages)

    def duplicat(self, port, l2_message, time, printing_flag):  # duplicate message for future flooding
        for out_port, link in enumerate(self.ports):
            if out_port != port and link is not None:
                duplicated_message = copy.copy(l2_message)
                self.enqueue(duplicated_message, out_port)

        if printing_flag == 1:
            print(f"Switch: {self.id} \033[35m Duplicated for future flood\033[0m the message (size: {l2_message.message_size}) "
                  f"at time: {time:.6f}")

    def print_statistics(self):
        print(f"Switch: {self.id} \033[32mTotal time\033[0m in the Head of Line: {self.totalHoLTime:.6f}")