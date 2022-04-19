import json
import logging

import requests

from common.common_consts.timeouts import SHORT_REQUEST_TIMEOUT
from infection_monkey.config import WormConfiguration
from infection_monkey.control import ControlClient
from infection_monkey.custom_types import PropagationCredentials
from infection_monkey.i_control_channel import IControlChannel, IslandCommunicationError

requests.packages.urllib3.disable_warnings()

logger = logging.getLogger(__name__)


class ControlChannel(IControlChannel):
    def __init__(self, server: str, agent_id: str):
        self._agent_id = agent_id
        self._control_channel_server = server

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
                proxies=ControlClient.proxies,
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

    def get_config(self) -> dict:
        try:
            response = requests.get(  # noqa: DUO123
                "https://%s/api/agent/%s" % (WormConfiguration.current_server, self._agent_id),
                verify=False,
                proxies=ControlClient.proxies,
                timeout=SHORT_REQUEST_TIMEOUT,
            )
            response.raise_for_status()

            return json.loads(response.content.decode())
        except (
            json.JSONDecodeError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.TooManyRedirects,
            requests.exceptions.HTTPError,
        ) as e:
            raise IslandCommunicationError(e)

    def get_credentials_for_propagation(self) -> PropagationCredentials:
        propagation_credentials_url = (
            f"https://{self._control_channel_server}/api/propagation-credentials/{self._agent_id}"
        )
        try:
            response = requests.get(  # noqa: DUO123
                propagation_credentials_url,
                verify=False,
                proxies=ControlClient.proxies,
                timeout=SHORT_REQUEST_TIMEOUT,
            )
            response.raise_for_status()

            return json.loads(response.content.decode())["propagation_credentials"]
        except (
            json.JSONDecodeError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.TooManyRedirects,
            requests.exceptions.HTTPError,
        ) as e:
            raise IslandCommunicationError(e)
