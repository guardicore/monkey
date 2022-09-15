import json
import logging
from pprint import pformat
from typing import Optional, Sequence
from uuid import UUID

import requests
from urllib3 import disable_warnings

from common import AgentRegistrationData
from common.agent_configuration import AgentConfiguration
from common.common_consts.timeouts import SHORT_REQUEST_TIMEOUT
from common.credentials import Credentials
from common.network.network_utils import get_local_interfaces
from infection_monkey.i_control_channel import IControlChannel, IslandCommunicationError
from infection_monkey.utils import agent_process
from infection_monkey.utils.ids import get_agent_id, get_machine_id

disable_warnings()  # noqa: DUO131

logger = logging.getLogger(__name__)


class ControlChannel(IControlChannel):
    def __init__(self, server: str, agent_id: str):
        self._agent_id = agent_id
        self._control_channel_server = server

    def register_agent(self, parent: Optional[UUID] = None):
        agent_registration_data = AgentRegistrationData(
            id=get_agent_id(),
            machine_hardware_id=get_machine_id(),
            start_time=agent_process.get_start_time(),
            # parent_id=parent,
            parent_id=None,  # None for now, until we change GUID to UUID
            cc_server=self._control_channel_server,
            network_interfaces=get_local_interfaces(),
        )

        try:
            url = f"https://{self._control_channel_server}/api/agents"
            response = requests.post(  # noqa: DUO123
                url,
                json=agent_registration_data.dict(simplify=True),
                verify=False,
                timeout=SHORT_REQUEST_TIMEOUT,
            )
            response.raise_for_status()
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.TooManyRedirects,
            requests.exceptions.HTTPError,
        ) as e:
            raise IslandCommunicationError(e)

    def should_agent_stop(self) -> bool:
        if not self._control_channel_server:
            logger.error("Agent should stop because it can't connect to the C&C server.")
            return True
        try:
            url = (
                f"https://{self._control_channel_server}/api/monkey-control"
                f"/needs-to-stop/{self._agent_id}"
            )
            response = requests.get(  # noqa: DUO123
                url,
                verify=False,
                timeout=SHORT_REQUEST_TIMEOUT,
            )
            response.raise_for_status()

            json_response = json.loads(response.content.decode())
            return json_response["stop_agent"]
        except (
            json.JSONDecodeError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.TooManyRedirects,
            requests.exceptions.HTTPError,
        ) as e:
            raise IslandCommunicationError(e)

    def get_config(self) -> AgentConfiguration:
        try:
            response = requests.get(  # noqa: DUO123
                f"https://{self._control_channel_server}/api/agent-configuration",
                verify=False,
                timeout=SHORT_REQUEST_TIMEOUT,
            )
            response.raise_for_status()

            config_dict = json.loads(response.text)

            logger.debug(f"Received configuration:\n{pformat(config_dict)}")

            return AgentConfiguration(**config_dict)
        except (
            json.JSONDecodeError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.TooManyRedirects,
            requests.exceptions.HTTPError,
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
