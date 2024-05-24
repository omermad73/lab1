import numpy as np
from Event import Event


class SimulationFunctions:
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
        return None

    @staticmethod
    def find_object(all_components, id):
        for component in all_components:
            if component.id == id:
                return component
        print("there is not such host or switch")
        return None

    @staticmethod
    def find_l2message(all_l2message, id):
        for l2message in all_l2message:
            if l2message.id == id:
                return l2message
        print("there is not such host")
        return None

    @staticmethod
    def simulation():
        pass
