from GNO import GNO

class Event(GNO):
    def __init__(self, scheduled_time, event_type, scheduling_object_id, next_object_id, message_id):
        super().__init__("Event")
        self.scheduled_time = scheduled_time
        self.event_type = event_type
        self.scheduling_object_id = scheduling_object_id
        self.next_object_id = next_object_id
        self.message_id = message_id

    # Getter and Setter for scheduled_time
    @property
    def scheduled_time(self):
        return self._scheduled_time

    @scheduled_time.setter
    def scheduled_time(self, value):
        self._scheduled_time = value

    # Getter and Setter for event_type
    @property
    def event_type(self):
        return self._event_type

    @event_type.setter
    def event_type(self, value):
        self._event_type = value

    # Getter and Setter for scheduling_object_id
    @property
    def scheduling_object_id(self):
        return self._scheduling_object_id

    @scheduling_object_id.setter
    def scheduling_object_id(self, value):
        self._scheduling_object_id = value

    # Getter and Setter for next_object_id
    @property
    def next_object_id(self):
        return self._next_object_id

    @next_object_id.setter
    def next_object_id(self, value):
        self._next_object_id = value

    # Getter and Setter for message_id
    @property
    def message_id(self):
        return self._message_id

    @message_id.setter
    def message_id(self, value):
        self._message_id = value
