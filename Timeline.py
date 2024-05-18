from Event import Event

class Timeline:
    def __init__(self):
        self.events = []

    def add_events(self, events):
        for event in events:
            self.add_event(event)

    def add_event(self, event):
        if not isinstance(event, Event):
            raise ValueError("Only Event instances can be added to the timeline.")
        self.events.append(event)
        self.sort_events()

    def done(self):  # finished with an event
        self.events.remove(self.events[0])

    def get_events(self):
        return self.events

    def sort_events(self):
        self.events.sort(key=lambda event: event.scheduled_time)

    def __str__(self):
        return '\n'.join([f"Event ID: {event.id}, Scheduled Time: {event.scheduled_time}, Type: {event.event_type}" for event in self.events])
