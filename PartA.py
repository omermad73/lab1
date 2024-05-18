import numpy as np
from Event import Event
from Link import Link
from Host import Host
from Timeline import Timeline
class PartA:

    @staticmethod
    def main():
        print("hello world")
        different_timeline = Timeline()
        host1 = Host(1, 1, 1, 2)
        host2 = Host(1, 1, 1, 2)
        mylink = Link(1, 1, 1, 1, 1)

        number_of_packets = 2000
        lambda_param = 0.5
        PartA.generate_times(host1.id, different_timeline, number_of_packets, lambda_param)
        PartA.generate_times(host2.id, different_timeline, number_of_packets, lambda_param)

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
            event = Event(time, "Creating", host_id)
            timeline.add_event(event)


# Run the main function when the script is executed
if __name__ == "__main__":
    PartA.main()
