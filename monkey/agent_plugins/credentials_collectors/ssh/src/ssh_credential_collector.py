import logging
from typing import Sequence

from common.credentials import Credentials
from common.event_queue import IAgentEventQueue
from common.types import AgentID
from infection_monkey.i_puppet import ICredentialsCollector

from .ssh_handler import get_ssh_info, to_credentials

logger = logging.getLogger(__name__)


class SSHCredentialCollector(ICredentialsCollector):
    """
    SSH keys credential collector
    """

    def __init__(self, agent_event_queue: IAgentEventQueue, agent_id: AgentID):
        self._agent_event_queue = agent_event_queue
        self._agent_id = agent_id

    def run(self, options=None, interrupt=None) -> Sequence[Credentials]:
        logger.info("Started scanning for SSH credentials")
        ssh_info = get_ssh_info(self._agent_event_queue, self._agent_id)
        logger.info("Finished scanning for SSH credentials")

        return to_credentials(ssh_info)
