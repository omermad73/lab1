import numpy as np
from Event import Event
from Host import Host
from Timeline import Timeline
from Link import Link
from SimulationFunctions import SimulationFunctions


class PartA:
    @staticmethod
    def main():
        print("hello world")
        # settings
        number_of_packets = 20
        lambda_param = 0.5
        min_payload_size = 10
        max_payload_size = 20
        printing_flag = 1
        terminate = 20  # [sec].  after this time the simulation is eliminated
        time = 0

        # start simulation
        different_timeline = Timeline()
        host1 = Host("00:00:00:00:00:01")
        host2 = Host("00:00:00:00:00:02")
        my_link = Link(host1, host2, 3)  # change the nic on the host too

        all_host = [host1, host2]
        all_l2messages = []

        SimulationFunctions.generate_times(host1.id, different_timeline, number_of_packets, lambda_param)
        SimulationFunctions.generate_times(host2.id, different_timeline, number_of_packets, lambda_param)
        event = different_timeline.events[0]

        #  the end is never the end is never the end is never the end is never the end is never the end is never the end
        while different_timeline.events[0].scheduled_time < terminate:
            event = different_timeline.events[0]
            if event.event_type == "create a message":
                host = SimulationFunctions.find_host(all_host, event.scheduling_object_id)
                if not isinstance(host, Host):
                    raise ValueError("there is event without real host (How the hell you succeed to do it?) ")
                host.create_message(different_timeline, all_host, all_l2messages, min_payload_size, max_payload_size, printing_flag, my_link)  # adding new event
                time = event.scheduled_time
                different_timeline.done()  # remove event

            elif event.event_type == "message received":
                host = SimulationFunctions.find_host(all_host, event.next_object_id)
                l2_message = SimulationFunctions.find_l2message(all_l2messages, event.message_id)
                if not isinstance(host, Host):
                    raise ValueError("there is event without real host (How the hell you succeed to do it?) ")
                host.handle_message(l2_message, event.scheduled_time, printing_flag)  # adding new event
                all_l2messages.remove(l2_message)  # remove the l2message
                different_timeline.done()  # remove event

            if not different_timeline.events:  # if there is no more events, the simulation is over
                time = terminate


# Run the main function when the script is executed
if __name__ == "__main__":
    PartA.main()
