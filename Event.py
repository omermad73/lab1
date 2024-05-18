class Event:
    def __init__(self, scheduled_time, event_type, scheduling_object_id, next_object_id=-1, message_id=-1):
        self.scheduled_time = scheduled_time
        self.event_type = event_type
        self.scheduling_object_id = scheduling_object_id  # the sender
        self.next_object_id = next_object_id  # the receiver. if id -1 there isn't next object
        self.message_id = message_id  # if id -1 there isn't message
