import logging
import queue
import threading
from typing import Set

import requests

# TODO: shouldn't leak implementation information; can we do this some other way?
from pubsub import pub

from common.common_consts.timeouts import MEDIUM_REQUEST_TIMEOUT
from common.events import AbstractAgentEvent
from common.utils import Timer

logger = logging.getLogger(__name__)


DEFAULT_TIME_PERIOD = 5
WAKES_PER_PERIOD = 4


class send_all_events_to_island:
    def __init__(self, server_address: str):
        self._server_address = server_address
        self._queue: queue.Queue[AbstractAgentEvent] = queue.Queue()

        self._send_to_island_thread = self._batch_and_send_events_thread(
            self._queue, self._server_address, DEFAULT_TIME_PERIOD
        )
        self._send_to_island_thread.start()

    def __call__(self, event: AbstractAgentEvent, topic=pub.AUTO_TOPIC):
        topic_name = topic.getName()
        self._queue.put(self._serialize_event(event, topic_name))

        logger.debug(f"Sending event of type {topic_name} to the Island at {self._server_address}")

    def _serialize_event(self, event: AbstractAgentEvent, topic_name: str):
        pass

    class _batch_and_send_events_thread:
        def __init__(self, queue_of_events: queue.Queue, server_address: str, time_period: int):
            self._queue = queue_of_events
            self._server_address = server_address
            self._time_period = time_period

            self._event_batch: Set = set()
            self._should_run_batch_and_send_thread = True

        def start(self):
            self._should_run_batch_and_send_thread = True
            self._batch_and_send_thread = threading.Thread(
                name="SendEventsToIslandInBatchesThread", target=self._manage_event_batches
            )
            self._batch_and_send_thread.start()

        def _manage_event_batches(self):
            timer = Timer()
            timer.set(self._time_period)

            self._event_batch = {}

            while self._should_run_batch_and_send_thread:
                self._add_next_event_to_batch()

                if timer.is_expired():
                    self._send_events_to_island()
                    timer.reset()
                    self._event_batch = {}

            self._send_remaining_events()

        def _add_next_event_to_batch(self):
            try:
                event = self._queue.get(block=True, timeout=self._time_period / WAKES_PER_PERIOD)
                self._event_batch.add(event)
            except queue.Empty:
                pass

        def _send_events_to_island(self):
            for serialized_event in self._event_batch:
                try:
                    requests.post(  # noqa: DUO123
                        "https://%s/api/events" % (self._server_address,),
                        data=serialized_event,
                        headers={"content-type": "application/json"},
                        verify=False,
                        timeout=MEDIUM_REQUEST_TIMEOUT,
                    )
                except Exception as exc:
                    logger.warning(
                        f"Exception caught when connecting to the Island at {self.server_address}"
                        f": {exc}"
                    )

        def _send_remaining_events(self):
            while not self._queue.empty():
                self._add_next_event_to_batch()

            self._send_events_to_island()

        def stop(self):
            self._should_run_batch_and_send_thread = False
            self._batch_and_send_thread.join()
