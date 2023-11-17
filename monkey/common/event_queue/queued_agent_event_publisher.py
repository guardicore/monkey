from multiprocessing import Queue

from monkeyevents import AbstractAgentEvent

from . import IAgentEventPublisher


class QueuedAgentEventPublisher(IAgentEventPublisher):
    def __init__(self, queue: Queue):
        self._queue = queue

    def publish(self, event: AbstractAgentEvent):
        self._queue.put(event)
