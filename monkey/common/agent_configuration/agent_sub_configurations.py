from dataclasses import dataclass
from typing import Dict, Tuple

from pydantic import PositiveFloat, PositiveInt, conint, validator

from common.base_models import MutableInfectionMonkeyBaseModel

from .validators import (
    validate_ip,
    validate_linux_filename,
    validate_subnet_range,
    validate_windows_filename,
)


@dataclass(frozen=True)
class CustomPBAConfiguration:
    """
    A configuration for custom post-breach actions

    Attributes:
        :param linux_command: Command to run on Linux victim machines. If a file is uploaded,
                              use this field to change its permissions, execute it, and/or delete it
                              Example: `chmod +x file.sh; ./file.sh; rm file.sh`
        :param linux_filename: Name of the file to upload on Linux victim machines
        :param windows_command: Command to run on Windows victim machines. If a file is uploaded,
                                use this field to change its permissions, execute it, and/or delete
                                it
                                Example: `file.bat & del file.bat`
        :param windows_filename: Name of the file to upload on Windows victim machines
    """

    linux_command: str
    linux_filename: str
    windows_command: str
    windows_filename: str


class Pydantic___CustomPBAConfiguration(MutableInfectionMonkeyBaseModel):
    """
    A configuration for custom post-breach actions

    Attributes:
        :param linux_command: Command to run on Linux victim machines. If a file is uploaded,
                              use this field to change its permissions, execute it, and/or delete it
                              Example: `chmod +x file.sh; ./file.sh; rm file.sh`
        :param linux_filename: Name of the file to upload on Linux victim machines
        :param windows_command: Command to run on Windows victim machines. If a file is uploaded,
                                use this field to change its permissions, execute it, and/or delete
                                it
                                Example: `file.bat & del file.bat`
        :param windows_filename: Name of the file to upload on Windows victim machines
    """

    linux_command: str
    linux_filename: str
    windows_command: str
    windows_filename: str

    @validator("linux_filename")
    def linux_filename_valid(cls, filename):
        validate_linux_filename(filename)
        return filename

    @validator("windows_filename")
    def windows_filename_valid(cls, filename):
        validate_windows_filename(filename)
        return filename


@dataclass(frozen=True)
class PluginConfiguration:
    """
    A configuration for plugins

    Attributes:
        :param name: Name of the plugin
                     Example: "ransomware"
        :param options: Any other information/configuration fields relevant to the plugin
                        Example: {
                            "encryption": {
                                "enabled": True,
                                "directories": {
                                    "linux_target_dir": "~/this_dir",
                                    "windows_target_dir": "C:\that_dir"
                                },
                            },
                            "other_behaviors": {
                                "readme": True
                            },
                        }
    """

    name: str
    options: Dict


class Pydantic___PluginConfiguration(MutableInfectionMonkeyBaseModel):
    """
    A configuration for plugins

    Attributes:
        :param name: Name of the plugin
                     Example: "ransomware"
        :param options: Any other information/configuration fields relevant to the plugin
                        Example: {
                            "encryption": {
                                "enabled": True,
                                "directories": {
                                    "linux_target_dir": "~/this_dir",
                                    "windows_target_dir": "C:\that_dir"
                                },
                            },
                            "other_behaviors": {
                                "readme": True
                            },
                        }
    """

    name: str
    options: Dict


@dataclass(frozen=True)
class ScanTargetConfiguration:
    """
    Configuration of network targets to scan and exploit

    Attributes:
        :param blocked_ips: IP's that won't be scanned
                            Example: ("1.1.1.1", "2.2.2.2")
        :param inaccessible_subnets: Subnet ranges that shouldn't be accessible for the agent
                                     Example: ("1.1.1.1", "2.2.2.2/24", "myserver")
        :param local_network_scan: Whether or not the agent should scan the local network
        :param subnets: Subnet ranges to scan
                        Example: ("192.168.1.1-192.168.2.255", "3.3.3.3", "2.2.2.2/24",
                                  "myHostname")
    """

    blocked_ips: Tuple[str, ...]
    inaccessible_subnets: Tuple[str, ...]
    local_network_scan: bool
    subnets: Tuple[str, ...]


class Pydantic___ScanTargetConfiguration(MutableInfectionMonkeyBaseModel):
    """
    Configuration of network targets to scan and exploit

    Attributes:
        :param blocked_ips: IP's that won't be scanned
                            Example: ("1.1.1.1", "2.2.2.2")
        :param inaccessible_subnets: Subnet ranges that shouldn't be accessible for the agent
                                     Example: ("1.1.1.1", "2.2.2.2/24", "myserver")
        :param local_network_scan: Whether or not the agent should scan the local network
        :param subnets: Subnet ranges to scan
                        Example: ("192.168.1.1-192.168.2.255", "3.3.3.3", "2.2.2.2/24",
                                  "myHostname")
    """

    blocked_ips: Tuple[str, ...]
    inaccessible_subnets: Tuple[str, ...]
    local_network_scan: bool
    subnets: Tuple[str, ...]

    @validator("blocked_ips", each_item=True)
    def blocked_ips_valid(cls, ip):
        validate_ip(ip)
        return ip

    @validator("inaccessible_subnets", each_item=True)
    def inaccessible_subnets_valid(cls, subnet_range):
        validate_subnet_range(subnet_range)
        return subnet_range

    @validator("subnets", each_item=True)
    def subnets_valid(cls, subnet_range):
        validate_subnet_range(subnet_range)
        return subnet_range


@dataclass(frozen=True)
class ICMPScanConfiguration:
    """
    A configuration for ICMP scanning

    Attributes:
        :param timeout: Maximum time in seconds to wait for a response from the target
    """

    timeout: float


class Pydantic___ICMPScanConfiguration(MutableInfectionMonkeyBaseModel):
    """
    A configuration for ICMP scanning

    Attributes:
        :param timeout: Maximum time in seconds to wait for a response from the target
    """

    timeout: PositiveFloat


@dataclass(frozen=True)
class TCPScanConfiguration:
    """
    A configuration for TCP scanning

    Attributes:
        :param timeout: Maximum time in seconds to wait for a response from the target
        :param ports: Ports to scan
    """

    timeout: float
    ports: Tuple[int, ...]


class Pydantic___TCPScanConfiguration(MutableInfectionMonkeyBaseModel):
    """
    A configuration for TCP scanning

    Attributes:
        :param timeout: Maximum time in seconds to wait for a response from the target
        :param ports: Ports to scan
    """

    timeout: PositiveFloat
    ports: Tuple[conint(ge=0, le=65535), ...]


@dataclass(frozen=True)
class NetworkScanConfiguration:
    """
    A configuration for network scanning

    Attributes:
        :param tcp: Configuration for TCP scanning
        :param icmp: Configuration for ICMP scanning
        :param fingerprinters: Configuration for fingerprinters to run
        :param targets: Configuration for targets to scan
    """

    tcp: TCPScanConfiguration
    icmp: ICMPScanConfiguration
    fingerprinters: Tuple[PluginConfiguration, ...]
    targets: ScanTargetConfiguration


class Pydantic___NetworkScanConfiguration(MutableInfectionMonkeyBaseModel):
    """
    A configuration for network scanning

    Attributes:
        :param tcp: Configuration for TCP scanning
        :param icmp: Configuration for ICMP scanning
        :param fingerprinters: Configuration for fingerprinters to run
        :param targets: Configuration for targets to scan
    """

    tcp: Pydantic___TCPScanConfiguration
    icmp: Pydantic___ICMPScanConfiguration
    fingerprinters: Tuple[Pydantic___PluginConfiguration, ...]
    targets: Pydantic___ScanTargetConfiguration


@dataclass(frozen=True)
class ExploitationOptionsConfiguration:
    """
    A configuration for exploitation options

    Attributes:
        :param http_ports: HTTP ports to exploit
    """

    http_ports: Tuple[int, ...]


class Pydantic___ExploitationOptionsConfiguration(MutableInfectionMonkeyBaseModel):
    """
    A configuration for exploitation options

    Attributes:
        :param http_ports: HTTP ports to exploit
    """

    http_ports: Tuple[conint(ge=0, le=65535), ...]


@dataclass(frozen=True)
class ExploitationConfiguration:
    """
    A configuration for exploitation

    Attributes:
        :param options: Exploitation options shared by all exploiters
        :param brute_force: Configuration for brute force exploiters
        :param vulnerability: Configuration for vulnerability exploiters
    """

    options: ExploitationOptionsConfiguration
    brute_force: Tuple[PluginConfiguration, ...]
    vulnerability: Tuple[PluginConfiguration, ...]


class Pydantic___ExploitationConfiguration(MutableInfectionMonkeyBaseModel):
    """
    A configuration for exploitation

    Attributes:
        :param options: Exploitation options shared by all exploiters
        :param brute_force: Configuration for brute force exploiters
        :param vulnerability: Configuration for vulnerability exploiters
    """

    options: Pydantic___ExploitationOptionsConfiguration
    brute_force: Tuple[Pydantic___PluginConfiguration, ...]
    vulnerability: Tuple[Pydantic___PluginConfiguration, ...]


@dataclass(frozen=True)
class PropagationConfiguration:
    """
    A configuration for propagation

    Attributes:
        :param maximum_depth: Maximum number of hops allowed to spread from the machine where
                              the attack started i.e. how far to propagate in the network from the
                              first machine
        :param network_scan: Configuration for network scanning
        :param exploitation: Configuration for exploitation
    """

    maximum_depth: int
    network_scan: NetworkScanConfiguration
    exploitation: ExploitationConfiguration


class Pydantic___PropagationConfiguration(MutableInfectionMonkeyBaseModel):
    """
    A configuration for propagation

    Attributes:
        :param maximum_depth: Maximum number of hops allowed to spread from the machine where
                              the attack started i.e. how far to propagate in the network from the
                              first machine
        :param network_scan: Configuration for network scanning
        :param exploitation: Configuration for exploitation
    """

    maximum_depth: PositiveInt
    network_scan: Pydantic___NetworkScanConfiguration
    exploitation: Pydantic___ExploitationConfiguration
