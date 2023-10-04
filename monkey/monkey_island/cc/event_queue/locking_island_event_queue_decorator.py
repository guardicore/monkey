from monkeytypes import RLock

from . import IIslandEventQueue, IslandEventSubscriber, IslandEventTopic


class LockingIslandEventQueueDecorator(IIslandEventQueue):
    """
    Makes an IIslandEventQueue thread-safe by locking publish()
    """

    def __init__(self, island_event_queue: IIslandEventQueue, lock: RLock):
        self._lock = lock
        self._island_event_queue = island_event_queue

    def subscribe(self, topic: IslandEventTopic, subscriber: IslandEventSubscriber):
        self._island_event_queue.subscribe(topic, subscriber)

    def publish(self, topic: IslandEventTopic, **kwargs):
        with self._lock:
            self._island_event_queue.publish(topic, **kwargs)
