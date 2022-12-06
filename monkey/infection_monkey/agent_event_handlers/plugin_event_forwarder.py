import logging
import queue
from contextlib import suppress
from multiprocessing import Queue
from threading import Event, Thread

from common.event_queue import IAgentEventQueue

logger = logging.getLogger(__name__)

QUEUE_EVENT_TIMEOUT = 2


class PluginEventForwarder(Thread):
    """
    Publishes events from the Agent's Plugin queue to the Agent's Event queue
    """

    def __init__(
        self,
        queue: Queue,
        agent_event_queue: IAgentEventQueue,
        queue_event_timeout: float = QUEUE_EVENT_TIMEOUT,
    ):
        self._queue = queue
        self._agent_event_queue = agent_event_queue
        self._queue_event_timeout = queue_event_timeout
        super().__init__(name="PluginEventForwarder", daemon=True)

        self._stop = Event()

    def run(self):
        logger.info("Starting plugin event forwarder")

        while not self._stop.is_set():
            with suppress(queue.Empty):
                event = self._queue.get(timeout=self._queue_event_timeout)
                self._agent_event_queue.publish(event)

    def stop(self):
        logger.info("Stopping plugin event forwarder")
        self._stop.set()
