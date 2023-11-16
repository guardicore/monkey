from typing import Type

from monkeyevents import AbstractAgentEvent
from monkeytypes import BasicLock

from . import AgentEventSubscriber, IAgentEventQueue


class LockingAgentEventQueueDecorator(IAgentEventQueue):
    """
    Makes an IAgentEventQueue thread-safe by locking publish()
    """

    def __init__(self, agent_event_queue: IAgentEventQueue, lock: BasicLock):
        self._lock = lock
        self._agent_event_queue = agent_event_queue

    def subscribe_all_events(self, subscriber: AgentEventSubscriber):
        self._agent_event_queue.subscribe_all_events(subscriber)

    def subscribe_type(
        self, event_type: Type[AbstractAgentEvent], subscriber: AgentEventSubscriber
    ):
        self._agent_event_queue.subscribe_type(event_type, subscriber)

    def subscribe_tag(self, tag: str, subscriber: AgentEventSubscriber):
        self._agent_event_queue.subscribe_tag(tag, subscriber)

    def publish(self, event: AbstractAgentEvent):
        with self._lock:
            self._agent_event_queue.publish(event)
