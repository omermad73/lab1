import numpy as np
from Event import Event
from Host import Host
from Timeline import Timeline
from Link import Link
from SimulationFunctions import SimulationFunctions
from Switch import Switch



class PartA:
    @staticmethod
    def main():
        # simulation settings
        number_of_packets = 20
        lambda_param = 0.5
        min_payload_size = 10
        max_payload_size = 20
        printing_flag = 1
        terminate = 30  # [sec] after this time the simulation is eliminated
        file_name = "macTableLog.txt"
        mac_table_log_file = open(file_name, 'w')

        # topology configuration
        different_timeline = Timeline()
        host1 = Host("00:00:00:00:00:01")
        host2 = Host("00:00:00:00:00:02")
        link1 = Link(host1, host2, 3)  # changes the nic on the host too


        all_host = [host1, host2]
        links = [link1]
        all_switches = []
        all_components = all_host + all_switches

        all_l2messages = []
        should_terminate = False

        host_link_map = {}  # Create host-link map
        for link in links:
            host_link_map[link.host1] = link
            host_link_map[link.host2] = link

        # start simulation
        for host in all_host:
            SimulationFunctions.generate_times(host.id, different_timeline, number_of_packets, lambda_param)

        #  main loop
        while not should_terminate and different_timeline.events[0].scheduled_time < terminate:
            event = different_timeline.events[0]
            if event.event_type == "create a message":
                host = SimulationFunctions.find_host(all_host, event.scheduling_object_id)
                if not isinstance(host, Host):
                    raise ValueError("there is event without real host (How the hell you succeed to do it?) ")
                host.create_message(different_timeline, all_host, all_l2messages, min_payload_size, max_payload_size, printing_flag, host_link_map[host])  # adding new event

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

        mac_table_log_file.close()


# Run the main function when the script is executed
if __name__ == "__main__":
    PartA.main()
