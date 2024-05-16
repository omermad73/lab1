import time

class PartA:
    startTime = time.time_ns()

    @staticmethod
    def main():
        # Create a new host
        host1 = Host(1, "00:00:00:00:00:01", 1)
        host2 = Host(2, "00:00:00:00:00:02", 2)

        # Create a new link
        link1 = Link(1, 2, 1000.0)

class Host:
    def __init__(self, host_id, mac, nic):
        self.host_id = host_id
        self.mac = mac
        self.nic = nic

class Link:
    def __init__(self, host1, host2, tx_rate):
        self.host1 = host1
        self.host2 = host2
        self.tx_rate = tx_rate

# Run the main function when the script is executed
if __name__ == "__main__":
    PartA.main()
