from ipaddress import IPv4Address

from common.types import NetworkPort, PortStatus

from . import AbstractAgentEvent


class TCPScanEvent(AbstractAgentEvent):
    """
    An event that occurs when the Agent performs a TCP scan on a host

    Attributes:
        :param port: Port on which the scan was performed
        :param port_status: Status of the port (closed/open)
        :param banner: Information from the TCP response
    """

    target: IPv4Address
    port: NetworkPort
    port_status: PortStatus
    banner: str
