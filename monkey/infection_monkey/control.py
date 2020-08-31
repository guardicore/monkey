import json
import logging
import platform
from socket import gethostname
from urllib.parse import urljoin

import requests
from requests.exceptions import ConnectionError

import infection_monkey.monkeyfs as monkeyfs
import infection_monkey.tunnel as tunnel
from common.data.api_url_consts import T1216_PBA_FILE_DOWNLOAD_PATH
from infection_monkey.config import GUID, WormConfiguration
from infection_monkey.network.info import check_internet_access, local_ips
from infection_monkey.transport.http import HTTPConnectProxy
from infection_monkey.transport.tcp import TcpProxy
from infection_monkey.utils.exceptions.planned_shutdown_exception import \
    PlannedShutdownException

__author__ = 'hoffer'


requests.packages.urllib3.disable_warnings()

LOG = logging.getLogger(__name__)
DOWNLOAD_CHUNK = 1024

PBA_FILE_DOWNLOAD = "https://%s/api/pba/download/%s"

# random number greater than 5,
# to prevent the monkey from just waiting forever to try and connect to an island before going elsewhere.
TIMEOUT_IN_SECONDS = 15


class ControlClient(object):
    proxies = {}

    @staticmethod
    def wakeup(parent=None, has_internet_access=None):
        if parent:
            LOG.debug("parent: %s" % (parent,))

        hostname = gethostname()
        if not parent:
            parent = GUID

        if has_internet_access is None:
            has_internet_access = check_internet_access(WormConfiguration.internet_services)

        monkey = {'guid': GUID,
                  'hostname': hostname,
                  'ip_addresses': local_ips(),
                  'description': " ".join(platform.uname()),
                  'internet_access': has_internet_access,
                  'config': WormConfiguration.as_dict(),
                  'parent': parent}

        if ControlClient.proxies:
            monkey['tunnel'] = ControlClient.proxies.get('https')

        requests.post("https://%s/api/monkey" % (WormConfiguration.current_server,),  # noqa: DUO123
                      data=json.dumps(monkey),
                      headers={'content-type': 'application/json'},
                      verify=False,
                      proxies=ControlClient.proxies,
                      timeout=20)

    @staticmethod
    def find_server(default_tunnel=None):
        LOG.debug("Trying to wake up with Monkey Island servers list: %r" % WormConfiguration.command_servers)
        if default_tunnel:
            LOG.debug("default_tunnel: %s" % (default_tunnel,))

        current_server = ""

        for server in WormConfiguration.command_servers:
            try:
                current_server = server

                debug_message = "Trying to connect to server: %s" % server
                if ControlClient.proxies:
                    debug_message += " through proxies: %s" % ControlClient.proxies
                LOG.debug(debug_message)
                requests.get("https://%s/api?action=is-up" % (server,),  # noqa: DUO123
                             verify=False,
                             proxies=ControlClient.proxies,
                             timeout=TIMEOUT_IN_SECONDS)
                WormConfiguration.current_server = current_server
                break

            except ConnectionError as exc:
                current_server = ""
                LOG.warning("Error connecting to control server %s: %s", server, exc)

        if current_server:
            return True
        else:
            if ControlClient.proxies:
                return False
            else:
                LOG.info("Starting tunnel lookup...")
                proxy_find = tunnel.find_tunnel(default=default_tunnel)
                if proxy_find:
                    proxy_address, proxy_port = proxy_find
                    LOG.info("Found tunnel at %s:%s" % (proxy_address, proxy_port))
                    ControlClient.proxies['https'] = 'https://%s:%s' % (proxy_address, proxy_port)
                    return ControlClient.find_server()
                else:
                    LOG.info("No tunnel found")
                    return False

    @staticmethod
    def keepalive():
        if not WormConfiguration.current_server:
            return
        try:
            monkey = {}
            if ControlClient.proxies:
                monkey['tunnel'] = ControlClient.proxies.get('https')
            requests.patch("https://%s/api/monkey/%s" % (WormConfiguration.current_server, GUID),  # noqa: DUO123
                           data=json.dumps(monkey),
                           headers={'content-type': 'application/json'},
                           verify=False,
                           proxies=ControlClient.proxies)
        except Exception as exc:
            LOG.warning("Error connecting to control server %s: %s",
                        WormConfiguration.current_server, exc)
            return {}

    @staticmethod
    def send_telemetry(telem_category, data):
        if not WormConfiguration.current_server:
            LOG.error("Trying to send %s telemetry before current server is established, aborting." % telem_category)
            return
        try:
            telemetry = {'monkey_guid': GUID, 'telem_category': telem_category, 'data': data}
            requests.post("https://%s/api/telemetry" % (WormConfiguration.current_server,),  # noqa: DUO123
                          data=json.dumps(telemetry),
                          headers={'content-type': 'application/json'},
                          verify=False,
                          proxies=ControlClient.proxies)
        except Exception as exc:
            LOG.warning("Error connecting to control server %s: %s",
                        WormConfiguration.current_server, exc)

    @staticmethod
    def send_log(log):
        if not WormConfiguration.current_server:
            return
        try:
            telemetry = {'monkey_guid': GUID, 'log': json.dumps(log)}
            requests.post("https://%s/api/log" % (WormConfiguration.current_server,),  # noqa: DUO123
                          data=json.dumps(telemetry),
                          headers={'content-type': 'application/json'},
                          verify=False,
                          proxies=ControlClient.proxies)
        except Exception as exc:
            LOG.warning("Error connecting to control server %s: %s",
                        WormConfiguration.current_server, exc)

    @staticmethod
    def load_control_config():
        if not WormConfiguration.current_server:
            return
        try:
            reply = requests.get("https://%s/api/monkey/%s" % (WormConfiguration.current_server, GUID),  # noqa: DUO123
                                 verify=False,
                                 proxies=ControlClient.proxies)

        except Exception as exc:
            LOG.warning("Error connecting to control server %s: %s",
                        WormConfiguration.current_server, exc)
            return

        try:
            unknown_variables = WormConfiguration.from_kv(reply.json().get('config'))
            LOG.info("New configuration was loaded from server: %r" %
                     (WormConfiguration.hide_sensitive_info(WormConfiguration.as_dict()),))
        except Exception as exc:
            # we don't continue with default conf here because it might be dangerous
            LOG.error("Error parsing JSON reply from control server %s (%s): %s",
                      WormConfiguration.current_server, reply._content, exc)
            raise Exception("Couldn't load from from server's configuration, aborting. %s" % exc)

        if unknown_variables:
            ControlClient.send_config_error()

    @staticmethod
    def send_config_error():
        if not WormConfiguration.current_server:
            return
        try:
            requests.patch("https://%s/api/monkey/%s" % (WormConfiguration.current_server, GUID),  # noqa: DUO123
                           data=json.dumps({'config_error': True}),
                           headers={'content-type': 'application/json'},
                           verify=False,
                           proxies=ControlClient.proxies)
        except Exception as exc:
            LOG.warning("Error connecting to control server %s: %s", WormConfiguration.current_server, exc)
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
            ControlClient.spoof_host_os_info(is_windows, is_32bit))
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

        return \
            {
                "os":
                    {
                        "type": os,
                        "machine": arch
                    }
            }

    @staticmethod
    def download_monkey_exe_by_filename(filename, size):
        if not WormConfiguration.current_server:
            return None
        try:
            dest_file = monkeyfs.virtual_path(filename)
            if (monkeyfs.isfile(dest_file)) and (size == monkeyfs.getsize(dest_file)):
                return dest_file
            else:
                download = requests.get("https://%s/api/monkey/download/%s" %  # noqa: DUO123
                                        (WormConfiguration.current_server, filename),
                                        verify=False,
                                        proxies=ControlClient.proxies)

                with monkeyfs.open(dest_file, 'wb') as file_obj:
                    for chunk in download.iter_content(chunk_size=DOWNLOAD_CHUNK):
                        if chunk:
                            file_obj.write(chunk)
                    file_obj.flush()
                if size == monkeyfs.getsize(dest_file):
                    return dest_file

        except Exception as exc:
            LOG.warning("Error connecting to control server %s: %s",
                        WormConfiguration.current_server, exc)

    @staticmethod
    def get_monkey_exe_filename_and_size_by_host(host):
        return ControlClient.get_monkey_exe_filename_and_size_by_host_dict(host.as_dict())

    @staticmethod
    def get_monkey_exe_filename_and_size_by_host_dict(host_dict):
        if not WormConfiguration.current_server:
            return None, None
        try:
            reply = requests.post("https://%s/api/monkey/download" % (WormConfiguration.current_server,),  # noqa: DUO123
                                  data=json.dumps(host_dict),
                                  headers={'content-type': 'application/json'},
                                  verify=False, proxies=ControlClient.proxies)
            if 200 == reply.status_code:
                result_json = reply.json()
                filename = result_json.get('filename')
                if not filename:
                    return None, None
                size = result_json.get('size')
                return filename, size
            else:
                return None, None

        except Exception as exc:
            LOG.warning("Error connecting to control server %s: %s",
                        WormConfiguration.current_server, exc)

        return None, None

    @staticmethod
    def create_control_tunnel():
        if not WormConfiguration.current_server:
            return None

        my_proxy = ControlClient.proxies.get('https', '').replace('https://', '')
        if my_proxy:
            proxy_class = TcpProxy
            try:
                target_addr, target_port = my_proxy.split(':', 1)
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
            return requests.get(PBA_FILE_DOWNLOAD %  # noqa: DUO123
                                (WormConfiguration.current_server, filename),
                                verify=False,
                                proxies=ControlClient.proxies)
        except requests.exceptions.RequestException:
            return False

    @staticmethod
    def get_T1216_pba_file():
        try:
            return requests.get(urljoin(f"https://{WormConfiguration.current_server}/",  # noqa: DUO123
                                        T1216_PBA_FILE_DOWNLOAD_PATH),
                                verify=False,
                                proxies=ControlClient.proxies,
                                stream=True)
        except requests.exceptions.RequestException:
            return False

    @staticmethod
    def should_monkey_run(vulnerable_port: str) -> bool:
        if vulnerable_port and \
           WormConfiguration.get_hop_distance_to_island() > 1 and \
           ControlClient.can_island_see_port(vulnerable_port) and \
           WormConfiguration.started_on_island:
            raise PlannedShutdownException("Monkey shouldn't run on current machine "
                                           "(it will be exploited later with more depth).")
        return True

    @staticmethod
    def can_island_see_port(port):
        try:
            url = f"https://{WormConfiguration.current_server}/api/monkey_control/check_remote_port/{port}"
            response = requests.get(url, verify=False)
            response = json.loads(response.content.decode())
            return response['status'] == "port_visible"
        except requests.exceptions.RequestException:
            return False

    @staticmethod
    def report_start_on_island():
        requests.post(f"https://{WormConfiguration.current_server}/api/monkey_control/started_on_island",
                      data=json.dumps({'started_on_island': True}),
                      verify=False)
