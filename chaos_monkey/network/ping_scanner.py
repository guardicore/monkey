
import os
import sys
import subprocess
from network import HostScanner
from model.host import VictimHost

__author__ = 'itamar'

PING_COUNT_FLAG = "-n" if "win32" == sys.platform else "-c"
PING_TIMEOUT_FLAG = "-w" if "win32" == sys.platform else "-W"

class PingScanner(HostScanner):
    def __init__(self):
        self._config = __import__('config').WormConfiguration
        self._devnull = open(os.devnull, "w")

    def is_host_alive(self, host):
        assert isinstance(host, VictimHost)

        return 0 == subprocess.call(["ping",
                                     PING_COUNT_FLAG, "1",
                                     PING_TIMEOUT_FLAG, str(self._config.ping_scan_timeout),
                                     host.ip_addr],
                                    stdout=self._devnull,
                                    stderr=self._devnull)
