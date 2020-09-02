import re

import infection_monkey.config
from infection_monkey.network.HostFinger import HostFinger
from infection_monkey.network.tools import check_tcp_port

SSH_PORT = 22
SSH_SERVICE_DEFAULT = 'tcp-22'
SSH_REGEX = r'SSH-\d\.\d-OpenSSH'
TIMEOUT = 10
BANNER_READ = 1024
LINUX_DIST_SSH = ['ubuntu', 'debian']


class SSHFinger(HostFinger):
    _SCANNED_SERVICE = 'SSH'

    def __init__(self):
        self._config = infection_monkey.config.WormConfiguration
        self._banner_regex = re.compile(SSH_REGEX, re.IGNORECASE)

    @staticmethod
    def _banner_match(service, host, banner):
        host.services[service]['name'] = 'ssh'
        for dist in LINUX_DIST_SSH:
            if banner.lower().find(dist) != -1:
                host.os['type'] = 'linux'
                os_version = banner.split(' ').pop().strip()
                if 'version' not in host.os:
                    host.os['version'] = os_version
                else:
                    host.services[service]['os-version'] = os_version
                break

    def get_host_fingerprint(self, host):

        for name, data in list(host.services.items()):
            banner = data.get('banner', '')
            if self._banner_regex.search(banner):
                self._banner_match(name, host, banner)
                host.services[SSH_SERVICE_DEFAULT]['display_name'] = self._SCANNED_SERVICE
                return

        is_open, banner = check_tcp_port(host.ip_addr, SSH_PORT, TIMEOUT, True)

        if is_open:
            self.init_service(host.services, SSH_SERVICE_DEFAULT, SSH_PORT)

            if banner:
                host.services[SSH_SERVICE_DEFAULT]['banner'] = banner
                if self._banner_regex.search(banner):
                    self._banner_match(SSH_SERVICE_DEFAULT, host, banner)
                return True

        return False
