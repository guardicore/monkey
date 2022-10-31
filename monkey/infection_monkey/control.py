import json
import logging
from socket import gethostname

import requests
from urllib3 import disable_warnings

from common.common_consts.timeouts import MEDIUM_REQUEST_TIMEOUT
from common.network.network_utils import get_my_ip_addresses_legacy
from common.types import SocketAddress
from infection_monkey.config import GUID
from infection_monkey.utils import agent_process

disable_warnings()  # noqa DUO131

logger = logging.getLogger(__name__)


class ControlClient:
    def __init__(self, server_address: SocketAddress):
        self.server_address = server_address

    def wakeup(self, parent=None):
        if parent:
            logger.debug("parent: %s" % (parent,))

        hostname = gethostname()
        if not parent:
            parent = GUID

        monkey = {
            "guid": GUID,
            "hostname": hostname,
            "ip_addresses": get_my_ip_addresses_legacy(),
            "parent": parent,
            "launch_time": agent_process.get_start_time(),
        }

        requests.post(  # noqa: DUO123
            f"https://{self.server_address}/api/agent",
            data=json.dumps(monkey),
            headers={"content-type": "application/json"},
            verify=False,
            timeout=MEDIUM_REQUEST_TIMEOUT,
        )
