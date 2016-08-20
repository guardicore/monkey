import re
from network import HostFinger
from network.tools import check_port_tcp
from model.host import VictimHost

SSH_PORT = 22
SSH_SERVICE_DEFAULT = 'tcp-22'
SSH_REGEX = 'SSH-\d\.\d-OpenSSH'
TIMEOUT = 10
BANNER_READ = 1024
LINUX_DIST_SSH = ['ubuntu', 'debian']


class SSHFinger(HostFinger):
    def __init__(self):
        self._config = __import__('config').WormConfiguration
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
        assert isinstance(host, VictimHost)

        for name, data in host.services.items():
            banner = data.get('banner', '')
            if self._banner_regex.search(banner):
                self._banner_match(name, host, banner)
                return

        is_open, banner = check_port_tcp(host.ip_addr, SSH_PORT, TIMEOUT, True)

        if is_open:
            host.services[SSH_SERVICE_DEFAULT] = {}

            if banner:
                host.services[SSH_SERVICE_DEFAULT]['banner'] = banner
                if self._banner_regex.search(banner):
                    self._banner_match(SSH_SERVICE_DEFAULT, host, banner)
                return True

        return False
