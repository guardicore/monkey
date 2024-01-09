import logging
import queue
from contextlib import suppress
from queue import Queue
from threading import Event

from monkeytoolbox import create_daemon_thread

from common.event_queue import IAgentEventQueue

logger = logging.getLogger(__name__)

QUEUE_EVENT_TIMEOUT = 2


class PluginEventForwarder:
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

        self._thread = create_daemon_thread(target=self.run, name="PluginEventForwarder")
        self._stop = Event()

    def start(self):
        """
        Starts the PluginEventForwarder in the background
        """
        self._stop.clear()
        self._thread.start()

    def run(self):
        """
        Publishes events that are on a queue

        Watch the queue for new events and forward them to the IAgentEventQueue. Block until
        `stop()` is called.
        """
        logger.info("Starting plugin event forwarder")

        while not self._stop.is_set():
            with suppress(queue.Empty):
                event = self._queue.get(timeout=self._queue_event_timeout)
                self._agent_event_queue.publish(event)

    def stop(self, timeout=None):
        """
        Stops the PluginEventForwarder

        When this function returns, all events on the queue will have been forwarded to the
        IAgentEventQueue.

        When the timeout argument is not present or None, the operation will block until the
        PluginEventForwarder stops.

        :param timeout: The number of seconds to wait for the PluginEventForwarder to stop
        """
        logger.info("Stopping plugin event forwarder")
        if self._thread.is_alive():
            self._stop.set()
            self._thread.join(timeout)
        self.flush()

    def flush(self):
        """
        Publishes the events until the queue is empty
        """
        while not self._queue.empty():
            event = self._queue.get(timeout=self._queue_event_timeout)
            self._agent_event_queue.publish(event)
