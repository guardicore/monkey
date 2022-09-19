import logging
from typing import Optional, Sequence
from uuid import UUID

import requests
from urllib3 import disable_warnings

from common import AgentRegistrationData
from common.agent_configuration import AgentConfiguration
from common.common_consts.timeouts import SHORT_REQUEST_TIMEOUT
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


class ControlChannel(IControlChannel):
    def __init__(self, server: str, agent_id: str, api_client: IIslandAPIClient):
        self._agent_id = agent_id
        self._control_channel_server = server
        self._island_api_client = api_client

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

        try:
            self._island_api_client.register_agent(agent_registration_data)
        except (IslandAPIConnectionError, IslandAPITimeoutError) as e:
            raise IslandCommunicationError(e)

    def should_agent_stop(self) -> bool:
        if not self._control_channel_server:
            logger.error("Agent should stop because it can't connect to the C&C server.")
            return True
        try:
            return self._island_api_client.should_agent_stop(
                self._control_channel_server, self._agent_id
            )
        except (
            IslandAPIConnectionError,
            IslandAPIRequestError,
            IslandAPIRequestFailedError,
            IslandAPITimeoutError,
        ) as e:
            raise IslandCommunicationError(e)

    def get_config(self) -> AgentConfiguration:
        try:
            return self._island_api_client.get_config(self._control_channel_server)
        except (
            IslandAPIConnectionError,
            IslandAPIRequestError,
            IslandAPIRequestFailedError,
            IslandAPITimeoutError,
        ) as e:
            raise IslandCommunicationError(e)

    def get_credentials_for_propagation(self) -> Sequence[Credentials]:
        propagation_credentials_url = (
            f"https://{self._control_channel_server}/api/propagation-credentials"
        )
        try:
            response = requests.get(  # noqa: DUO123
                propagation_credentials_url,
                verify=False,
                timeout=SHORT_REQUEST_TIMEOUT,
            )
            response.raise_for_status()

            return [Credentials(**credentials) for credentials in response.json()]
        except (
            requests.exceptions.JSONDecodeError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.TooManyRedirects,
            requests.exceptions.HTTPError,
        ) as e:
            raise IslandCommunicationError(e)
