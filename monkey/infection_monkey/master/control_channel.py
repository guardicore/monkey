import logging
from functools import wraps
from typing import Sequence

from urllib3 import disable_warnings

from common.agent_configuration import AgentConfiguration
from common.credentials import Credentials
from common.types import AgentID
from infection_monkey.i_control_channel import IControlChannel, IslandCommunicationError
from infection_monkey.island_api_client import IIslandAPIClient, IslandAPIError

disable_warnings()  # noqa: DUO131

logger = logging.getLogger(__name__)


def handle_island_api_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IslandAPIError as err:
            raise IslandCommunicationError(err)

    return wrapper


class ControlChannel(IControlChannel):
    def __init__(self, server: str, agent_id: AgentID, api_client: IIslandAPIClient):
        self._agent_id = agent_id
        self._control_channel_server = server
        self._island_api_client = api_client

    @handle_island_api_errors
    def should_agent_stop(self) -> bool:
        if not self._control_channel_server:
            logger.error("Agent should stop because it can't connect to the C&C server.")
            return True
        agent_signals = self._island_api_client.get_agent_signals(self._agent_id)
        return agent_signals.terminate is not None

    @handle_island_api_errors
    def get_config(self) -> AgentConfiguration:
        return self._island_api_client.get_config()

    @handle_island_api_errors
    def get_credentials_for_propagation(self) -> Sequence[Credentials]:
        return self._island_api_client.get_credentials_for_propagation()
