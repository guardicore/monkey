import logging

import requests

# TODO: shouldn't leak implementation information; can we do this some other way?
from pubsub import pub

from common.common_consts.timeouts import MEDIUM_REQUEST_TIMEOUT
from common.events import AbstractAgentEvent

logger = logging.getLogger(__name__)


class push_all_events_to_island:
    def __init__(self, server_address: str):
        self._server_address = server_address

    def __call__(self, event: AbstractAgentEvent, topic=pub.AUTO_TOPIC):
        requests.post(  # noqa: DUO123
            "https://%s/api/events" % (self._server_address,),
            data=self._serialize_event(event, topic.getName()),
            headers={"content-type": "application/json"},
            verify=False,
            timeout=MEDIUM_REQUEST_TIMEOUT,
        )

    def _serialize_event(self, event: AbstractAgentEvent, topic_name: str):
        pass
