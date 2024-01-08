import logging
import queue
import threading

from monkeyevents import AbstractAgentEvent
from monkeytoolbox import PeriodicCaller

from infection_monkey.island_api_client import IIslandAPIClient

logger = logging.getLogger(__name__)


DEFAULT_TIME_PERIOD_SECONDS = 5


class AgentEventForwarder:
    """
    Sends information about the events carried out by the Agent to the Island in batches
    """

    def __init__(
        self,
        island_api_client: IIslandAPIClient,
    ):
        self._batching_agent_event_forwarder = BatchingAgentEventForwarder(island_api_client)
        self._periodic_caller = PeriodicCaller(
            self._batching_agent_event_forwarder.flush,
            DEFAULT_TIME_PERIOD_SECONDS,
            name="AgentEventForwarder",
        )

    def start(self):
        self._periodic_caller.start()

    def stop(self):
        # Make sure we flush all events before stopping, otherwise the events will get lost
        self.flush()

        self._periodic_caller.stop()

    def send_event(self, event: AbstractAgentEvent):
        """
        Send an event to the Island

        :param event: An event to be sent to the Island
        """
        logger.debug(
            f"Adding event of type {type(event).__name__} to the queue to send to the Island"
        )
        self._batching_agent_event_forwarder.add_event_to_queue(event)

    def flush(self):
        """
        Forward all events to the Island

        When this method returns, all events that were published prior to the method call are
        guaranteed to have been sent to the Island.
        """
        self._batching_agent_event_forwarder.flush()


class BatchingAgentEventForwarder:
    """
    Handles the batching and sending of the Agent's events to the Island
    """

    def __init__(self, island_api_client: IIslandAPIClient):
        self._island_api_client = island_api_client

        self._queue: queue.Queue[AbstractAgentEvent] = queue.Queue()
        self._send_lock = threading.Lock()

    def add_event_to_queue(self, agent_event: AbstractAgentEvent):
        self._queue.put(agent_event)

    def flush(self):
        # This method could be called simultaneously from different threads. For example,
        # the PeriodicCaller calls flush() at the same time as flush() is called from another
        # thread (likely the main thread).
        #
        # The goal of this lock is to ensure that when flush() returns, the queue has been fully
        # flushed. Without the lock, it may be possible that the PeriodicCaller has built a list of
        # events to send and these have not been sent to the island at the time when flush()
        # returns.
        with self._send_lock:
            if self._queue.empty():
                return

            events = []

            while not self._queue.empty():
                events.append(self._queue.get(block=False))

            try:
                logger.debug(f"Sending {len(events)} Agent events to the Island: {events}")
                self._island_api_client.send_events(events)
            except Exception:
                logger.exception("Exception caught when connecting to the Island")

                # Put all unsent events back on the queue so we can attempt to resend them later
                for event in events:
                    self._queue.put(event)
