import logging
import queue

import requests

# TODO: shouldn't leak implementation information; can we do this some other way?
from pubsub import pub

from common.common_consts.timeouts import MEDIUM_REQUEST_TIMEOUT
from common.events import AbstractAgentEvent

logger = logging.getLogger(__name__)


class push_all_events_to_island:
    def __init__(self, server_address: str):
        self._server_address = server_address

        self._queue: queue.Queue[AbstractAgentEvent] = queue.Queue()
        self._send_to_island_thread = self.batch_events_thread(self._queue, self._server_address)

        self._send_to_island_thread.start()

    def __call__(self, event: AbstractAgentEvent, topic=pub.AUTO_TOPIC):
        topic_name = topic.getName()

        self._queue.put(self._serialize_event(event, topic_name))

        logger.debug(f"Pushing event of type {topic_name} to the Island at {self._server_address}")

    def _serialize_event(self, event: AbstractAgentEvent, topic_name: str):
        pass

    class batch_events_thread:
        def __init__(self, queue_of_events: queue.Queue, server_address: str):
            self._queue = queue_of_events
            self._server_address = server_address

        def start(self):
            pass

        def _manage_next_event(self):
            pass

        def _send_event_to_island(self, serialized_event):
            requests.post(  # noqa: DUO123
                "https://%s/api/events" % (self._server_address,),
                data=serialized_event,
                headers={"content-type": "application/json"},
                verify=False,
                timeout=MEDIUM_REQUEST_TIMEOUT,
            )

        def stop(self):
            pass
