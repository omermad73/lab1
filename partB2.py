import random
from Event import Event
from Host import Host
from Timeline import Timeline
from Link import Link
from SimulationFunctions import SimulationFunctions
from Switch import Switch


class PartB2:
    @staticmethod
    def main():
        # simulation settings
        number_of_packets = 20
        lambda_param = 0.5
        min_payload_size = 10
        max_payload_size = 20
        printing_flag = 1
        terminate = 100  # [sec] after this time the simulation is eliminated
        file_name = "macTableLog.txt"
        mac_table_log_file = open(file_name, 'w')
        mac_table_log_file = None

        # topology configuration
        different_timeline = Timeline()
        num_hosts0 = random.randint(2, 4)
        num_hosts1 = random.randint(2, 4)
        port_num_s0 = 8
        port_num_s1 = 8
        # Creating switches
        switch0 = Switch(port_num_s0, 10, mac_table_log_file)
        switch1 = Switch(port_num_s1, num_hosts0 + num_hosts1 - 2, mac_table_log_file)
        # Creating hosts
        left_hosts = SimulationFunctions.create_hosts(0, num_hosts0)
        right_hosts = SimulationFunctions.create_hosts(num_hosts0, num_hosts1)
        hosts = left_hosts + right_hosts
        # Creating links
        links = []
        switch0_links = []
        switch1_links = []
        for host in left_hosts:
            link = Link(host, switch0, 3)
            links.append(link)
            switch0_links.append(link)
        for host in right_hosts:
            link = Link(host, switch1, 3)
            links.append(link)
            switch1_links.append(link)
        switches_link = Link(switch0, switch1)  # The link between the two switches
        links.append(switches_link)
        switch0_links.append(switches_link)
        switch1_links.append(switches_link)

        switch0.connect_all_ports(switch0_links)
        switch1.connect_all_ports(switch1_links)
        switches = [switch0, switch1]
        all_components = hosts + switches

        print(f"number of hosts connected to switch0: {num_hosts0}")
        print(f"number of hosts connected to switch1: {num_hosts1}")

        # start simulation
        all_l2messages = []
        should_terminate = False

        host_link_map = {}  # Create host-link map
        for link in links:
            host_link_map[link.host1] = link
            host_link_map[link.host2] = link

        for host in hosts:
            SimulationFunctions.generate_times(host.id, different_timeline, number_of_packets, lambda_param)

        #  main loop
        while not should_terminate and different_timeline.events[0].scheduled_time < terminate:
            event = different_timeline.events[0]
            if event.event_type == "create a message":
                host = SimulationFunctions.find_host(hosts, event.scheduling_object_id)
                if not isinstance(host, Host):
                    raise ValueError("there is event without real host (How the hell you succeed to do it?) ")
                host.create_message(different_timeline, hosts, all_l2messages, min_payload_size, max_payload_size, printing_flag, host_link_map[host])  # adding new event
                different_timeline.done()  # remove event

            elif event.event_type == "message received":
                receiver = SimulationFunctions.find_object(all_components, event.next_object_id)
                l2_message = SimulationFunctions.find_l2message(all_l2messages, event.message_id)
                if not isinstance(receiver, Host) and not isinstance(receiver, Switch):
                    raise ValueError("there is event without real host or switch (How the hell you succeed to do it?) ")
                receiver.handle_message(l2_message, all_l2messages, different_timeline, event.scheduled_time, event.link_id, printing_flag)
                all_l2messages.remove(l2_message)  # remove the l2message
                different_timeline.done()  # remove event

            if not different_timeline.events:  # if there is no more events, the simulation is over
                should_terminate = True
                print("Simulation ended successfully")

        if mac_table_log_file is not None:
            mac_table_log_file.close()


# Run the main function when the script is executed
if __name__ == "__main__":
    PartB2.main()
