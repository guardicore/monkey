import pytest
from monkeytypes import PortStatus

from common.types import NetworkPort
from infection_monkey.i_puppet import PortScanData, PortScanDataDict


def test_port_scan_data_dict__constructor():
    input_dict = {
        NetworkPort(1): PortScanData(port=1, status=PortStatus.OPEN),
        NetworkPort(2): PortScanData(port=2, status=PortStatus.CLOSED),
        NetworkPort(3): PortScanData(port=3, status=PortStatus.OPEN),
    }
    expected_port_scan_data_dict = {
        1: PortScanData(port=1, status=PortStatus.OPEN),
        2: PortScanData(port=2, status=PortStatus.CLOSED),
        3: PortScanData(port=3, status=PortStatus.OPEN),
    }

    port_scan_data_dict: PortScanDataDict = PortScanDataDict(input_dict)

    assert port_scan_data_dict == expected_port_scan_data_dict


def test_port_scan_data_dict__set():
    expected_port_scan_data_dict = {
        1: PortScanData(port=1, status=PortStatus.OPEN),
        2: PortScanData(port=2, status=PortStatus.CLOSED),
    }

    port_scan_data_dict = PortScanDataDict()
    port_scan_data_dict[1] = PortScanData(port=1, status=PortStatus.OPEN)
    port_scan_data_dict[2] = PortScanData(port=2, status=PortStatus.CLOSED)

    assert port_scan_data_dict == expected_port_scan_data_dict


INVALID_PORTS = (-1, 65536, "string", None, "22.2")
VALID_PORT_SCAN_DATA = PortScanData(port=1, status=PortStatus.OPEN)


@pytest.mark.parametrize("invalid_port", INVALID_PORTS)
def test_port_scan_data_dict_constructor__invalid_port(invalid_port):
    with pytest.raises((ValueError, TypeError)):
        PortScanDataDict({invalid_port: VALID_PORT_SCAN_DATA})


@pytest.mark.parametrize("invalid_port", INVALID_PORTS)
def test_port_scan_data_dict_update__invalid_port(invalid_port):
    port_scan_data_dict = PortScanDataDict()
    with pytest.raises((ValueError, TypeError)):
        port_scan_data_dict.update({invalid_port: VALID_PORT_SCAN_DATA})


@pytest.mark.parametrize("invalid_port", INVALID_PORTS)
def test_port_scan_data_dict_set__invalid_port(invalid_port):
    port_scan_data_dict = PortScanDataDict()
    with pytest.raises((ValueError, TypeError)):
        port_scan_data_dict[invalid_port] = VALID_PORT_SCAN_DATA


def test_closed_tcp_ports():
    expected_closed_ports = {2, 4}
    tcp_ports = PortScanDataDict(
        {
            NetworkPort(1): PortScanData(port=1, status=PortStatus.OPEN),
            NetworkPort(2): PortScanData(port=2, status=PortStatus.CLOSED),
            NetworkPort(3): PortScanData(port=3, status=PortStatus.OPEN),
            NetworkPort(4): PortScanData(port=4, status=PortStatus.CLOSED),
        }
    )

    assert tcp_ports.closed == expected_closed_ports


def test_open_tcp_ports():
    expected_open_ports = {1, 3}
    tcp_ports = PortScanDataDict(
        {
            NetworkPort(1): PortScanData(port=1, status=PortStatus.OPEN),
            NetworkPort(2): PortScanData(port=2, status=PortStatus.CLOSED),
            NetworkPort(3): PortScanData(port=3, status=PortStatus.OPEN),
            NetworkPort(4): PortScanData(port=4, status=PortStatus.CLOSED),
        }
    )

    assert tcp_ports.open == expected_open_ports
