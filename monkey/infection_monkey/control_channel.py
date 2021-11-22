import json
import logging
from abc import ABC

import requests

from common.common_consts.timeouts import SHORT_REQUEST_TIMEOUT
from infection_monkey.config import GUID, WormConfiguration
from monkey.infection_monkey.i_control_channel import IControlChannel

requests.packages.urllib3.disable_warnings()

logger = logging.getLogger(__name__)


class ControlChannel(IControlChannel, ABC):
    def should_agent_stop(self) -> bool:
        server = WormConfiguration.current_server
        if not server:
            return

        try:
            response = requests.get(  # noqa: DUO123
                f"{server}/api/monkey_control/{GUID}",
                verify=False,
                timeout=SHORT_REQUEST_TIMEOUT,
            )

            response = json.loads(response.content.decode())
            return response["stop_agent"]
        except Exception as e:
            logger.error(f"Error happened while trying to connect to server. {e}")
