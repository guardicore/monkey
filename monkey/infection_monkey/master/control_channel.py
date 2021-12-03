import json
import logging

import requests

from common.common_consts.timeouts import SHORT_REQUEST_TIMEOUT
from infection_monkey.config import WormConfiguration
from infection_monkey.control import ControlClient
from monkey.infection_monkey.i_control_channel import IControlChannel

requests.packages.urllib3.disable_warnings()

logger = logging.getLogger(__name__)


class ControlChannel(IControlChannel):
    def __init__(self, server: str, agent_id: str):
        self._agent_id = agent_id
        self._control_channel_server = server

    def should_agent_stop(self) -> bool:
        try:
            response = requests.get(  # noqa: DUO123
                f"{self._control_channel_server}/api/monkey_control/{self._agent_id}",
                verify=False,
                proxies=ControlClient.proxies,
                timeout=SHORT_REQUEST_TIMEOUT,
            )

            response = json.loads(response.content.decode())
            return response["stop_agent"]
        except Exception as e:
            # TODO: Evaluate how this exception is handled; don't just log and ignore it.
            logger.error(f"An error occurred while trying to connect to server. {e}")

        return True

    def get_config(self) -> dict:
        try:
            response = requests.get(  # noqa: DUO123
                "https://%s/api/monkey/%s" % (WormConfiguration.current_server, self._agent_id),
                verify=False,
                proxies=ControlClient.proxies,
                timeout=SHORT_REQUEST_TIMEOUT,
            )

            return json.loads(response.content.decode())
        except Exception as exc:
            # TODO: Evaluate how this exception is handled; don't just log and ignore it.
            logger.warning(
                "Error connecting to control server %s: %s", WormConfiguration.current_server, exc
            )

        return {}

    def get_credentials_for_propagation(self) -> dict:
        try:
            response = requests.get(  # noqa: DUO123
                f"{self._control_channel_server}/api/propagationCredentials",
                verify=False,
                proxies=ControlClient.proxies,
                timeout=SHORT_REQUEST_TIMEOUT,
            )

            response = json.loads(response.content.decode())["propagation_credentials"]
            return response
        except Exception as e:
            # TODO: Evaluate how this exception is handled; don't just log and ignore it.
            logger.error(f"An error occurred while trying to connect to server. {e}")
