from multiprocessing import Queue

from agentpluginapi import IAgentEventPublisher
from monkeyevents import AbstractAgentEvent


class QueuedAgentEventPublisher(IAgentEventPublisher):
    def __init__(self, queue: Queue):
        self._queue = queue

    def publish(self, event: AbstractAgentEvent):
        self._queue.put(event)
