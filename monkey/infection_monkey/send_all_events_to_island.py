import logging
import queue
import threading
from time import sleep

import requests

from common.common_consts.timeouts import MEDIUM_REQUEST_TIMEOUT
from common.events import AbstractAgentEvent

logger = logging.getLogger(__name__)


DEFAULT_TIME_PERIOD_SECONDS = 5
EVENTS_API_URL = "https://%s/api/events"


class send_all_events_to_island:
    """
    Sends information about the events carried out by the Agent to the Island in batches
    """

    def __init__(self, server_address: str):
        self._server_address = server_address
        self._queue: queue.Queue[AbstractAgentEvent] = queue.Queue()

        self._send_to_island_thread = self._batch_and_send_events_thread(
            self._queue, self._server_address, DEFAULT_TIME_PERIOD_SECONDS
        )
        self._send_to_island_thread.start()

    def __call__(self, event: AbstractAgentEvent):
        self._queue.put(self._serialize_event(event))
        logger.debug(
            f"Sending event of type {type(event).__name__} to the Island at {self._server_address}"
        )

    def _serialize_event(self, event: AbstractAgentEvent):
        pass

    class _batch_and_send_events_thread:
        """
        Handles the batching and sending of the Agent's events to the Island
        """

        def __init__(self, queue_of_events: queue.Queue, server_address: str, time_period: int):
            self._queue = queue_of_events
            self._server_address = server_address
            self._time_period = time_period

            self._should_run_batch_and_send_thread = True

        def start(self):
            self._should_run_batch_and_send_thread = True
            self._batch_and_send_thread = threading.Thread(
                name="SendEventsToIslandInBatchesThread", target=self._manage_event_batches
            )
            self._batch_and_send_thread.start()

        def _manage_event_batches(self):
            while self._should_run_batch_and_send_thread:
                self._send_events_to_island()
                sleep(self._time_period)

            self._send_remaining_events()

        def _send_events_to_island(self):
            if self._queue.empty():
                return

            events = []

            while not self._queue.empty():
                events.append(self._queue.get(block=False))

            try:
                requests.post(  # noqa: DUO123
                    EVENTS_API_URL % (self._server_address,),
                    json=events,
                    verify=False,
                    timeout=MEDIUM_REQUEST_TIMEOUT,
                )
            except Exception as exc:
                logger.warning(
                    f"Exception caught when connecting to the Island at {self._server_address}"
                    f": {exc}"
                )

        def _send_remaining_events(self):
            self._send_events_to_island()

        def stop(self):
            self._should_run_batch_and_send_thread = False
            self._batch_and_send_thread.join()
