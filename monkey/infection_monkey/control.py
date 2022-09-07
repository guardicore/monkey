import json
import logging
import platform
import socket
from socket import gethostname
from typing import Mapping, Optional, Sequence

import requests
from requests.exceptions import ConnectionError

import infection_monkey.tunnel as tunnel
from common.common_consts.timeouts import LONG_REQUEST_TIMEOUT, MEDIUM_REQUEST_TIMEOUT
from common.network.network_utils import address_to_ip_port
from infection_monkey.config import GUID
from infection_monkey.network.info import get_host_subnets, local_ips
from infection_monkey.network.relay import RELAY_CONTROL_MESSAGE
from infection_monkey.transport.http import HTTPConnectProxy
from infection_monkey.transport.tcp import TcpProxy
from infection_monkey.utils import agent_process
from infection_monkey.utils.environment import is_windows_os
from infection_monkey.utils.threading import create_daemon_thread

requests.packages.urllib3.disable_warnings()

logger = logging.getLogger(__name__)

PBA_FILE_DOWNLOAD = "https://%s/api/pba/download/%s"


class ControlClient:
    # TODO When we have mechanism that support telemetry messenger
    # with control clients, then this needs to be removed
    # https://github.com/guardicore/monkey/blob/133f7f5da131b481561141171827d1f9943f6aec/monkey/infection_monkey/telemetry/base_telem.py
    control_client_object = None

    def __init__(self, server_address: str, proxies: Optional[Mapping[str, str]] = None):
        self.proxies = {} if not proxies else proxies
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

    def find_server(self, servers: Sequence[str]):
        logger.debug(f"Trying to wake up with servers: {', '.join(servers)}")

        server_iterator = (s for s in servers)

        for server in server_iterator:

            try:
                debug_message = f"Trying to connect to server: {server}"
                logger.debug(debug_message)
                requests.get(  # noqa: DUO123
                    f"https://{server}/api?action=is-up",
                    verify=False,
                    timeout=MEDIUM_REQUEST_TIMEOUT,
                )

                break
                # TODO: Check how we are going to set the server address that the ControlCLient
                # is going to use
                # self.server_address = server
            except ConnectionError as err:
                logger.error(f"Unable to connect to server/relay {server}: {err}")
            except TimeoutError as err:
                logger.error(f"Timed out while connecting to server/relay {server}: {err}")
            except Exception as err:
                logger.error(
                    f"Exception encountered when trying to connect to server/relay {server}: {err}"
                )

        for server in server_iterator:
            t = create_daemon_thread(
                target=ControlClient._send_relay_control_message,
                name="SendControlRelayMessageThread",
                args=(server,),
            )
            t.start()

    @staticmethod
    def _send_relay_control_message(server: str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as d_socket:
            d_socket.settimeout(MEDIUM_REQUEST_TIMEOUT)

            try:
                address, port = address_to_ip_port(server)
                d_socket.connect((address, int(port)))
                d_socket.send(RELAY_CONTROL_MESSAGE)
                logger.info(f"Control message was sent to the server/relay {server}")
            except OSError as err:
                logger.error(f"Error connecting to socket {server}: {err}")

    def set_proxies(self, proxy_find):
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
                proxies=self.proxies,
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
                proxies=self.proxies,
                timeout=MEDIUM_REQUEST_TIMEOUT,
            )
        except Exception as exc:
            logger.warning(f"Error connecting to control server {self.server_address}: {exc}")

    def create_control_tunnel(self, keep_tunnel_open_time: int):
        if not self.server_address:
            return None

        my_proxy = self.proxies.get("https", "").replace("https://", "")
        if my_proxy:
            proxy_class = TcpProxy
            try:
                target_addr, target_port = my_proxy.split(":", 1)
                target_port = int(target_port)
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

    def get_pba_file(self, filename):
        try:
            return requests.get(  # noqa: DUO123
                PBA_FILE_DOWNLOAD % (self.server_address, filename),
                verify=False,
                proxies=self.proxies,
                timeout=LONG_REQUEST_TIMEOUT,
            )
        except requests.exceptions.RequestException:
            return False
