import logging
from typing import Any, Mapping, Sequence

from common.credentials import Credentials
from common.event_queue import IAgentEventPublisher
from common.types import AgentID, Event

from .chrome_credentials_collector_builder import build_chrome_credentials_collector

logger = logging.getLogger(__name__)


class Plugin:
    def __init__(self, *, agent_id: AgentID, agent_event_publisher: IAgentEventPublisher, **kwargs):
        self._agent_id = agent_id
        self._agent_event_publisher = agent_event_publisher

    def run(
        self, *, options: Mapping[str, Any], interrupt: Event, **kwargs
    ) -> Sequence[Credentials]:
        logger.info("Started scanning for Chrome-based browser credentials")

        try:
            chrome_credentials_collector = build_chrome_credentials_collector(
                self._agent_id, self._agent_event_publisher
            )
        except Exception as err:
            msg = (
                "An unexpected error occurred while building "
                f"the Chrome credentials collector: {err}"
            )
            logger.exception(msg)
            return []

        try:
            credentials = chrome_credentials_collector.run(interrupt)
            return credentials
        except Exception as err:
            msg = (
                "An unexpected error occurred while running "
                f"the Chrome credentials collector: {err}"
            )
            logger.exception(msg)
            return []
