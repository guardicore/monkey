import logging
from typing import Any, Mapping, Sequence

from common.credentials import Credentials
from common.event_queue import IAgentEventPublisher
from common.types import AgentID, Event

from .ssh_handler import get_ssh_info, to_credentials

logger = logging.getLogger(__name__)


class Plugin:
    def __init__(self, *, agent_id: AgentID, agent_event_publisher: IAgentEventPublisher, **kwargs):
        self._agent_id = agent_id
        self._agent_event_publisher = agent_event_publisher

    def run(
        self, *, options=Mapping[str, Any], interrupt: Event, **kwargs
    ) -> Sequence[Credentials]:
        logger.info("Started scanning for SSH credentials")
        ssh_info = get_ssh_info(self._agent_event_publisher, self._agent_id)
        logger.info("Finished scanning for SSH credentials")

        return to_credentials(ssh_info)
