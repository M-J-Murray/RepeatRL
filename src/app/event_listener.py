
class EventListener(object):
    events = dict()

    @classmethod
    def add_listener(cls, event_id, listener):
        if event_id in cls.events:
            raise Exception("Attempted to add listener '"+event_id+"' that already exists")
        cls.events[event_id] = listener

    @classmethod
    def trigger_event(cls, event_id, *args):
        if event_id not in cls.events:
            raise Exception("Attempted to trigger event '"+event_id+"' that doesn't exist")
        cls.events[event_id](*args)

    @classmethod
    def delete_listener(cls, event_id):
        if event_id not in cls.events:
            raise Exception("Attempted to delete event '"+event_id+"' that doesn't exist")
        del cls.events[event_id]

    @classmethod
    def rename_listener(cls, event_id, new_id):
        if event_id not in cls.events:
            raise Exception("Attempted to rename event '"+event_id+"' that doesn't exist")
        if new_id in cls.events:
            raise Exception("Attempted to rename event '" + event_id + "' to '"+new_id+"', but new id already exists")
        cls.events[new_id] = cls.events[event_id]
        del cls.events[event_id]
