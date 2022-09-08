import json
import logging
import platform
from socket import gethostname

import requests
from urllib3 import disable_warnings

from common.common_consts.timeouts import LONG_REQUEST_TIMEOUT, MEDIUM_REQUEST_TIMEOUT
from infection_monkey.config import GUID
from infection_monkey.network.info import get_host_subnets, local_ips
from infection_monkey.utils import agent_process

disable_warnings()  # noqa DUO131

logger = logging.getLogger(__name__)

PBA_FILE_DOWNLOAD = "https://%s/api/pba/download/%s"


class ControlClient:
    # TODO When we have mechanism that support telemetry messenger
    # with control clients, then this needs to be removed
    # https://github.com/guardicore/monkey/blob/133f7f5da131b481561141171827d1f9943f6aec/monkey/infection_monkey/telemetry/base_telem.py
    control_client_object = None

    def __init__(self, server_address: str):
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
            "ip_addresses": local_ips(),
            "networks": get_host_subnets(),
            "description": " ".join(platform.uname()),
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

    def send_telemetry(self, telem_category, json_data: str):
        if not self.server_address:
            logger.error(
                "Trying to send %s telemetry before current server is established, aborting."
                % telem_category
            )
            return
        try:
            telemetry = {"monkey_guid": GUID, "telem_category": telem_category, "data": json_data}
            requests.post(  # noqa: DUO123
                "https://%s/api/telemetry" % (self.server_address,),
                data=json.dumps(telemetry),
                headers={"content-type": "application/json"},
                verify=False,
                timeout=MEDIUM_REQUEST_TIMEOUT,
            )
        except Exception as exc:
            logger.warning(f"Error connecting to control server {self.server_address}: {exc}")

    def send_log(self, log):
        if not self.server_address:
            return
        try:
            telemetry = {"monkey_guid": GUID, "log": json.dumps(log)}
            requests.post(  # noqa: DUO123
                "https://%s/api/log" % (self.server_address,),
                data=json.dumps(telemetry),
                headers={"content-type": "application/json"},
                verify=False,
                timeout=MEDIUM_REQUEST_TIMEOUT,
            )
        except Exception as exc:
            logger.warning(f"Error connecting to control server {self.server_address}: {exc}")

    def get_pba_file(self, filename):
        try:
            return requests.get(  # noqa: DUO123
                PBA_FILE_DOWNLOAD % (self.server_address, filename),
                verify=False,
                timeout=LONG_REQUEST_TIMEOUT,
            )
        except requests.exceptions.RequestException:
            return False
