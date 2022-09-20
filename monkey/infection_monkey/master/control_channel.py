import logging
from functools import wraps
from typing import Optional, Sequence
from uuid import UUID

from urllib3 import disable_warnings

from common import AgentRegistrationData
from common.agent_configuration import AgentConfiguration
from common.credentials import Credentials
from common.network.network_utils import get_network_interfaces
from infection_monkey.i_control_channel import IControlChannel, IslandCommunicationError
from infection_monkey.island_api_client import (
    IIslandAPIClient,
    IslandAPIConnectionError,
    IslandAPIRequestError,
    IslandAPIRequestFailedError,
    IslandAPITimeoutError,
)
from infection_monkey.utils import agent_process
from infection_monkey.utils.ids import get_agent_id, get_machine_id

disable_warnings()  # noqa: DUO131

logger = logging.getLogger(__name__)


def handle_island_api_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            print(args)
            func(*args, **kwargs)
        except (
            IslandAPIConnectionError,
            IslandAPIRequestError,
            IslandAPIRequestFailedError,
            IslandAPITimeoutError,
        ) as e:
            raise IslandCommunicationError(e)

    return wrapper


class ControlChannel(IControlChannel):
    def __init__(self, server: str, agent_id: str, api_client: IIslandAPIClient):
        self._agent_id = agent_id
        self._control_channel_server = server
        self._island_api_client = api_client

    @handle_island_api_errors
    def register_agent(self, parent: Optional[UUID] = None):
        agent_registration_data = AgentRegistrationData(
            id=get_agent_id(),
            machine_hardware_id=get_machine_id(),
            start_time=agent_process.get_start_time(),
            # parent_id=parent,
            parent_id=None,  # None for now, until we change GUID to UUID
            cc_server=self._control_channel_server,
            network_interfaces=get_network_interfaces(),
        )

        self._island_api_client.register_agent(agent_registration_data)

    @handle_island_api_errors
    def should_agent_stop(self) -> bool:
        if not self._control_channel_server:
            logger.error("Agent should stop because it can't connect to the C&C server.")
            return True
        return self._island_api_client.should_agent_stop(self._agent_id)

    @handle_island_api_errors
    def get_config(self) -> AgentConfiguration:
        return self._island_api_client.get_config()

    @handle_island_api_errors
    def get_credentials_for_propagation(self) -> Sequence[Credentials]:
        return self._island_api_client.get_credentials_for_propagation()
