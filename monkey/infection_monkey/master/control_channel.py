import json
import logging
from pprint import pformat
from typing import Mapping, Sequence

import requests

from common.common_consts.timeouts import SHORT_REQUEST_TIMEOUT
from common.configuration import AgentConfiguration
from common.credentials import Credentials
from infection_monkey.i_control_channel import IControlChannel, IslandCommunicationError

requests.packages.urllib3.disable_warnings()

logger = logging.getLogger(__name__)


class ControlChannel(IControlChannel):
    def __init__(self, server: str, agent_id: str, proxies: Mapping[str, str]):
        self._agent_id = agent_id
        self._control_channel_server = server
        self._proxies = proxies

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
                proxies=self._proxies,
                timeout=SHORT_REQUEST_TIMEOUT,
            )
            response.raise_for_status()

            response = json.loads(response.content.decode())
            return response["stop_agent"]
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
                proxies=self._proxies,
                timeout=SHORT_REQUEST_TIMEOUT,
            )
            response.raise_for_status()

            logger.debug(f"Received configuration:\n{pformat(json.loads(response.text))}")

            return AgentConfiguration.from_json(response.text)
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
                proxies=self._proxies,
                timeout=SHORT_REQUEST_TIMEOUT,
            )
            response.raise_for_status()

            return [Credentials.from_mapping(credentials) for credentials in response.json()]
        except (
            requests.exceptions.JSONDecodeError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.TooManyRedirects,
            requests.exceptions.HTTPError,
        ) as e:
            raise IslandCommunicationError(e)
