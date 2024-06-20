from Switch import Switch


class SwitchLab2(Switch):
    def __init__(self, num_ports, mac_table_size, q_type, is_fluid=False, schedule_alg='FIFO', log_file=None, ttl=10):
        super().__init__(num_ports, mac_table_size, log_file, ttl)
        self.q_type = q_type
        self.is_fluid = is_fluid
        self.schedule_alg = schedule_alg
        self.queues = self.configure_queues()
        self.totalHoLTime = 0

    def configure_queues(self):
        if self.q_type == 'input':
            return [[] for _ in range(self.num_ports)]
        elif self.q_type == 'output':
            return [[] for _ in range(self.num_ports)]
        elif self.q_type == 'virtual_output':
            return [[[] for _ in range(self.num_ports)] for _ in range(self.num_ports)]

    def enqueue(self, packet, port):
