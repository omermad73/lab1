import numpy as np
from Event import Event
from Link import Link
from Host import Host
from Timeline import Timeline


class PartA:
    @staticmethod
    def main():
        print("hello world")
        # settings
        number_of_packets = 2
        lambda_param = 0.5
        min_payload_size = 10
        max_payload_size = 20
        printing_flag = 1
        terminate = 20  # [sec].  after this time the simulation is eliminated
        time = 0

        # start simulation
        different_timeline = Timeline()
        host1 = Host("00:00:00:00:00:01", 1, 1, 2)
        host2 = Host("00:00:00:00:00:02", 1, 1, 2)
        mylink = Link(host1, host2, 1, 1, 1)

        all_host = [host1, host2]

        PartA.generate_times(host1.id, different_timeline, number_of_packets, lambda_param)
        PartA.generate_times(host2.id, different_timeline, number_of_packets, lambda_param)
        event = different_timeline.events[0]

        i = 0
        #  the end is never the end is never the end is never the end is never the end is never the end is never the end
        while time < terminate:
            if event.event_type == "create a message":
                host = PartA.find_host(all_host, event.scheduling_object_id)
                if not isinstance(host, Host):
                    raise ValueError("there is event without real host (How the hell you succeed to do it?) ")
                host.create_l2_message(different_timeline, all_host, min_payload_size, max_payload_size, printing_flag)  # adding new event
                time = event.scheduled_time
                different_timeline.done()  # remove event
                if not different_timeline.events:  # if there is no more events, the simulation is over
                    time = terminate

    @staticmethod
    def generate_times(host_id, timeline, number_of_packets=2000, lambda_param=0.5):
        # generate the times between the L2 Messages
        # number_of_packets - Set the number of packets
        # lambda_param - Set the Input rate parameter for the exponential distributions
        # Generate realizations

        inter_arrival_times = np.random.exponential(scale=1 / lambda_param, size=number_of_packets)  # step 1

        # Calculate the input timeline
        arrival_times = np.cumsum(inter_arrival_times)  # step 2
        for time in arrival_times:  # step 3
            event = Event(time, "create a message", host_id)
            timeline.add_event(event)

    @staticmethod
    def find_host(all_host, id):
        for host in all_host:
            if host.id == id:
                return host
        print("there is not such host")
        return None  # null


# Run the main function when the script is executed
if __name__ == "__main__":
    PartA.main()
