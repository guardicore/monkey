from common.types import NetworkPort, PortStatus
from infection_monkey.i_puppet import PortScanData, TargetHostPorts


def test_closed_tcp_ports():
    expected_closed_ports = {NetworkPort(2), NetworkPort(4)}
    tcp_ports = {
        NetworkPort(1): PortScanData(port=NetworkPort(1), status=PortStatus.OPEN),
        NetworkPort(2): PortScanData(port=NetworkPort(2), status=PortStatus.CLOSED),
        NetworkPort(3): PortScanData(port=NetworkPort(3), status=PortStatus.OPEN),
        NetworkPort(4): PortScanData(port=NetworkPort(4), status=PortStatus.CLOSED),
    }
    thp = TargetHostPorts(tcp_ports=tcp_ports)

    assert thp.closed_tcp_ports == expected_closed_ports
