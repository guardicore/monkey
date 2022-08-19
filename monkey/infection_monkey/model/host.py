from typing import Optional

from common import OperatingSystem


class VictimHost(object):
    def __init__(self, ip_addr: str, domain_name: str = ""):
        self.ip_addr = ip_addr
        self.domain_name = str(domain_name)
        self.os = {}
        self.services = {}
        self.icmp = False
        self.default_tunnel = None
        self.default_server = None

    def as_dict(self):
        return self.__dict__

    def is_windows(self) -> bool:
        return OperatingSystem.WINDOWS == self.os["type"]

    def __hash__(self):
        return hash(self.ip_addr)

    def __eq__(self, other):
        if not isinstance(other, VictimHost):
            return False

        return self.ip_addr.__eq__(other.ip_addr)

    def __cmp__(self, other):
        if not isinstance(other, VictimHost):
            return -1

        return self.ip_addr.__cmp__(other.ip_addr)

    def __repr__(self):
        return "VictimHost({0!r})".format(self.ip_addr)

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
