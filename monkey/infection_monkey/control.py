import json
import logging
import platform
from socket import gethostname
from typing import MutableMapping, Optional, Tuple

import requests
from requests.exceptions import ConnectionError

import infection_monkey.tunnel as tunnel
from common.common_consts.timeouts import LONG_REQUEST_TIMEOUT, MEDIUM_REQUEST_TIMEOUT
from infection_monkey.config import GUID
from infection_monkey.network.info import get_host_subnets, local_ips
from infection_monkey.transport.http import HTTPConnectProxy
from infection_monkey.transport.tcp import TcpProxy
from infection_monkey.utils import agent_process
from infection_monkey.utils.environment import is_windows_os

logger = logging.getLogger(__name__)

PBA_FILE_DOWNLOAD = "https://%s/api/pba/download/%s"


class ControlClient:
    # TODO When we have mechanism that support telemetry messenger
    # with control clients, then this needs to be removed
    # https://github.com/guardicore/monkey/blob/133f7f5da131b481561141171827d1f9943f6aec/monkey/infection_monkey/telemetry/base_telem.py
    control_client_object = None

    def __init__(self, server_address: str, proxies: Optional[MutableMapping[str, str]] = None):
        self.proxies = {} if not proxies else proxies
        self.server_address = server_address

    def wakeup(self, parent: str = None):
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

        if self.proxies:
            monkey["tunnel"] = self.proxies.get("https")

        requests.post(  # noqa: DUO123
            f"https://{self.server_address}/api/agent",
            data=json.dumps(monkey),
            headers={"content-type": "application/json"},
            verify=False,
            proxies=self.proxies,
            timeout=MEDIUM_REQUEST_TIMEOUT,
        )

    def find_server(self, default_tunnel: str = None) -> bool:
        logger.debug(f"Trying to wake up with Monkey Island server: {self.server_address}")
        if default_tunnel:
            logger.debug("default_tunnel: %s" % (default_tunnel,))

        try:
            debug_message = "Trying to connect to server: %s" % self.server_address
            if self.proxies:
                debug_message += " through proxies: %s" % self.proxies
            logger.debug(debug_message)
            requests.get(  # noqa: DUO123
                f"https://{self.server_address}/api?action=is-up",
                verify=False,
                proxies=self.proxies,
                timeout=MEDIUM_REQUEST_TIMEOUT,
            )
            return True
        except ConnectionError as exc:
            logger.warning("Error connecting to control server %s: %s", self.server_address, exc)

        if self.proxies:
            return False
        else:
            logger.info("Starting tunnel lookup...")
            proxy_find = tunnel.find_tunnel(default=default_tunnel)
            if proxy_find:
                self.set_proxies(proxy_find)
                return self.find_server()
            else:
                logger.info("No tunnel found")
                return False

    def set_proxies(self, proxy_find: Tuple[str, str]):
        """
        Note: The proxy schema changes between different versions of requests and urllib3,
        which causes the machine to not open a tunnel back.
        If we get "ValueError: check_hostname requires server_hostname" or
        "Proxy URL had not schema, should start with http:// or https://" errors,
        the proxy schema needs to be changed.
        Keep this in mind when upgrading to newer python version or when urllib3 and
        requests are updated there is possibility that the proxy schema is changed.
        https://github.com/psf/requests/issues/5297
        https://github.com/psf/requests/issues/5855
        """
        proxy_address, proxy_port = proxy_find
        logger.info("Found tunnel at %s:%s" % (proxy_address, proxy_port))
        if is_windows_os():
            self.proxies["https"] = f"http://{proxy_address}:{proxy_port}"
        else:
            self.proxies["https"] = f"{proxy_address}:{proxy_port}"

    def send_telemetry(self, telem_category: str, json_data: str):
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
                proxies=self.proxies,
                timeout=MEDIUM_REQUEST_TIMEOUT,
            )
        except Exception as exc:
            logger.warning(f"Error connecting to control server {self.server_address}: {exc}")

    def send_log(self, log: str):
        if not self.server_address:
            return
        try:
            telemetry = {"monkey_guid": GUID, "log": json.dumps(log)}
            requests.post(  # noqa: DUO123
                "https://%s/api/log" % (self.server_address,),
                data=json.dumps(telemetry),
                headers={"content-type": "application/json"},
                verify=False,
                proxies=self.proxies,
                timeout=MEDIUM_REQUEST_TIMEOUT,
            )
        except Exception as exc:
            logger.warning(f"Error connecting to control server {self.server_address}: {exc}")

    def create_control_tunnel(self, keep_tunnel_open_time: int) -> Optional[tunnel.MonkeyTunnel]:
        if not self.server_address:
            return None

        my_proxy = self.proxies.get("https", "").replace("https://", "")
        if my_proxy:
            proxy_class = TcpProxy
            try:
                target_addr, target_port_str = my_proxy.split(":", 1)
                target_port = int(target_port_str)
            except ValueError:
                return None
        else:
            proxy_class = HTTPConnectProxy
            target_addr, target_port = None, None

        return tunnel.MonkeyTunnel(
            proxy_class,
            keep_tunnel_open_time=keep_tunnel_open_time,
            target_addr=target_addr,
            target_port=target_port,
        )

    def get_pba_file(self, filename: str):
        try:
            return requests.get(  # noqa: DUO123
                PBA_FILE_DOWNLOAD % (self.server_address, filename),
                verify=False,
                proxies=self.proxies,
                timeout=LONG_REQUEST_TIMEOUT,
            )
        except requests.exceptions.RequestException:
            return False
