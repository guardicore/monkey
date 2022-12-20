from typing import Any, Dict, Optional

from common import OperatingSystem


class TargetHost(object):
    def __init__(self, ip_addr: str):
        self.ip_addr = ip_addr
        self.os: Dict[str, Any] = {}
        self.services: Dict[str, Any] = {}
        self.icmp = False
        self.default_server = None

    def is_windows(self) -> bool:
        return OperatingSystem.WINDOWS == self.os["type"]

    def __hash__(self):
        return hash(self.ip_addr)

    def __eq__(self, other):
        if not isinstance(other, TargetHost):
            return False

        return self.ip_addr.__eq__(other.ip_addr)

    def __cmp__(self, other):
        if not isinstance(other, TargetHost):
            return -1

        return self.ip_addr.__cmp__(other.ip_addr)

    def __repr__(self):
        return "TargetHost({0!r})".format(self.ip_addr)

    def __str__(self):
        victim = "Victim Host %s: " % self.ip_addr
        victim += "OS - ["
        for k, v in list(self.os.items()):
            victim += "%s-%s " % (k, v)
        victim += "] Services - ["
        for k, v in list(self.services.items()):
            victim += "%s-%s " % (k, v)
        victim += "] ICMP: %s " % (self.icmp)
        return victim

    def set_island_address(self, ip: str, port: Optional[str]):
        self.default_server = f"{ip}:{port}" if port else f"{ip}"
