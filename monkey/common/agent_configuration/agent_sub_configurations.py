from typing import Dict, Tuple

from monkeytypes import MutableInfectionMonkeyBaseModel
from pydantic import BeforeValidator, Field, PositiveFloat
from typing_extensions import Annotated

from common.types import NetworkPort

from .validators import validate_ip, validate_subnet_range


class PluginConfiguration(MutableInfectionMonkeyBaseModel):
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


def _subnet_validator(subnet_range: str):
    validate_subnet_range(subnet_range)
    return subnet_range


def _ip_validator(ip: str):
    validate_ip(ip)
    return ip


Subnet = Annotated[str, BeforeValidator(_subnet_validator)]
BlockedIP = Annotated[str, BeforeValidator(_ip_validator)]


class ScanTargetConfiguration(MutableInfectionMonkeyBaseModel):
    """
    Configuration of network targets to scan and exploit

    Attributes:
        :param scan_my_networks: If true the Agent will scan networks it belongs to
         in addition to the provided subnet ranges
        :param subnets: Subnet ranges to scan
                        Example: ("192.168.1.1-192.168.2.255", "3.3.3.3", "2.2.2.2/24",
                                  "myHostname")
        :param blocked_ips: IP's that won't be scanned
                            Example: ("1.1.1.1", "2.2.2.2")
        :param inaccessible_subnets: Subnet ranges that shouldn't be accessible for the agent
                                     Example: ("1.1.1.1", "2.2.2.2/24", "myserver")
    """

    scan_my_networks: bool = Field(
        title="Scan Agent's networks",
        default=False,
        warning_message="If the Agent runs on a machine that has a publicly-facing network "
        "interface, this setting could cause scanning and exploitation of systems outside your "
        "organization.",
    )
    subnets: Tuple[Subnet, ...] = Field(
        title="Scan target list",
        description="List of targets the Monkey will try to scan. Targets can be "
        "IPs, subnets or hosts. "
        "Examples:\n"
        '\tTarget a specific IP: "192.168.0.1"\n'
        "\tTarget a subnet using a network range: "
        '"192.168.0.5-192.168.0.20"\n'
        '\tTarget a subnet using an IP mask: "192.168.0.5/24"\n'
        '\tTarget a specific host: "printer.example"',
        default=[],
    )
    blocked_ips: Tuple[BlockedIP, ...] = Field(
        title="Blocked IPs", description="List of IPs that the monkey will not scan.", default=[]
    )
    inaccessible_subnets: Tuple[Subnet, ...] = Field(
        title="Network segmentation testing",
        description="Test for network segmentation by providing a list of network segments "
        "that should not be accessible to each other.\n\n "
        "For example, if you configured the following three segments: "
        '"10.0.0.0/24", "11.0.0.2/32" and "12.2.3.0/24",'
        "a Monkey running on 10.0.0.5 will try to access machines in "
        "the following subnets: "
        "11.0.0.2/32, 12.2.3.0/24. An alert on successful cross-segment "
        "connections "
        "will be shown in the reports. \n\n"
        "Network segments can be IPs, subnets or hosts. Examples:\n"
        '\tDefine a single-IP segment: "192.168.0.1"\n'
        "\tDefine a segment using a network range: "
        '"192.168.0.5-192.168.0.20"\n'
        '\tDefine a segment using an subnet IP mask: "192.168.0.5/24"\n'
        '\tDefine a single-host segment: "printer.example"\n\n \u26A0'
        "Note that the networks configured in this section will be scanned using "
        "ping sweep.",
        default=[],
    )


class ICMPScanConfiguration(MutableInfectionMonkeyBaseModel):
    """
    A configuration for ICMP scanning

    Attributes:
        :param timeout: Maximum time in seconds to wait for a response from the target
    """

    timeout: PositiveFloat = Field(
        title="Ping scan timeout",
        description="Maximum time to wait for ping response in seconds",
        default=1.0,
    )


class TCPScanConfiguration(MutableInfectionMonkeyBaseModel):
    """
    A configuration for TCP scanning

    Attributes:
        :param ports: Ports to scan
        :param timeout: Maximum time in seconds to wait for a response from the target
    """

    ports: Tuple[NetworkPort, ...] = Field(
        title="TCP target ports",
        description="List of TCP ports the monkey will check whether they're open",
        default=[22, 2222, 445, 135, 389, 80, 8080, 443, 8008, 3306, 7001, 8088, 5885, 5986],
    )
    timeout: PositiveFloat = Field(
        title="TCP scan timeout",
        description="Maximum time to wait for TCP response in seconds",
        default=3.0,
    )


class NetworkScanConfiguration(MutableInfectionMonkeyBaseModel):
    """
    A configuration for network scanning

    Attributes:
        :param targets: Configuration for targets to scan
        :param icmp: Configuration for ICMP scanning
        :param tcp: Configuration for TCP scanning
        :param fingerprinters: Configuration for fingerprinters to run
    """

    targets: ScanTargetConfiguration = Field(
        title="Network",
        description='If "Scan Agent\'s networks" is checked, the Monkey scans for machines '
        "on each of the network interfaces of the machine it is running "
        "on.\nAdditionally, the Monkey scans "
        'machines according to "Scan target list" and skips machines in '
        '"Blocked IPs".',
    )
    icmp: ICMPScanConfiguration = Field(
        title="Ping scanner", description="Configure ICMP scanning options"
    )
    tcp: TCPScanConfiguration = Field(
        title="TCP scanner", description="Configure TCP scanning options"
    )
    fingerprinters: Tuple[PluginConfiguration, ...] = Field(
        title="Fingerprinters",
        description="Fingerprint modules collect info about external "
        "services that Infection Monkey scans.",
    )


class ExploitationOptionsConfiguration(MutableInfectionMonkeyBaseModel):
    """
    A configuration for exploitation options

    Attributes:
        :param http_ports: HTTP ports to exploit
    """

    http_ports: Tuple[NetworkPort, ...] = Field(
        title="HTTP ports",
        description="List of ports the Agent will check for using an HTTP protocol",
        default=[80, 8080, 443, 8008, 7001, 8983, 9600],
    )


class ExploitationConfiguration(MutableInfectionMonkeyBaseModel):
    """
    A configuration for exploitation

    Attributes:
        :param exploiters: Configuration enabled exploiters
        :param options: Exploitation options shared by all exploiters
    """

    exploiters: Dict[str, Dict] = Field(
        title="Enabled exploiters",
        description="Click on an exploiter to get more information"
        " about it. \n \u26A0 Note that using unsafe exploits may"
        " cause crashes of the exploited machine/service.",
    )
    options: ExploitationOptionsConfiguration = Field(
        title="Exploiters options",
        description="Configure exploitation options shared by all exploiters",
    )


class PropagationConfiguration(MutableInfectionMonkeyBaseModel):
    """
    A configuration for propagation

    Attributes:
        :param maximum_depth: Maximum number of hops allowed to spread from the machine where
                              the attack started i.e. how far to propagate in the network from the
                              first machine
        :param network_scan: Configuration for network scanning
        :param exploitation: Configuration for exploitation
    """

    maximum_depth: Annotated[int, Field(ge=0)] = Field(  # type: ignore[valid-type]
        title="Maximum scan depth",
        description="Amount of hops allowed for the monkey to spread from the "
        "Island server. \n \u26A0"
        " Note that setting this value too high may result in the "
        'Monkey propagating too far, if "Scan Agent\'s networks" is enabled.\n'
        "Setting this to 0 will disable all scanning and exploitation.",
        default=2,
    )
    network_scan: NetworkScanConfiguration = Field(
        title="Network analysis",
        description="Configure the network analysis that the Agents will perform",
    )
    exploitation: ExploitationConfiguration = Field(
        title="Exploiters", description="Configure the exploitation step of the attack"
    )


class PolymorphismConfiguration(MutableInfectionMonkeyBaseModel):
    """
    A configuration for polymorphism

    Attributes:
        :param randomize_agent_hash: If true, the Agent will emulate the property of polymorphism
                                      that all copies have unique hashes
    """

    randomize_agent_hash: bool = Field(
        title="Randomize Agent hash",
        description="Emulate the property of polymorphic (or metamorphic) malware that all "
        "copies have unique hashes.",
        default=False,
    )
