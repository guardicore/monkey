from ipaddress import IPv4Address, IPv4Interface
from pathlib import Path
from typing import Optional

from monkeytypes import InfectionMonkeyBaseModel, OperatingSystem

from infection_monkey.network.tools import get_interface_to_target


class LocalMachineInfo(InfectionMonkeyBaseModel):
    """
    Contains information about the local machine

    :param operating_system: Operating system of the local machine
    :param temporary_directory: Path to a temporary directory on the local machine
                                to store artifacts
    :param network_interfaces: Network interfaces on the local machine
    """

    operating_system: OperatingSystem
    temporary_directory: Path
    network_interfaces: frozenset[IPv4Interface]

    def get_interface_to_target(self, target: IPv4Address) -> Optional[IPv4Interface]:
        """
        Gets an interface on the local machine that can be reached by the target machine
        """
        return get_interface_to_target(self.network_interfaces, target)
