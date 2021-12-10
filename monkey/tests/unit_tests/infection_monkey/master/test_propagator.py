from threading import Event

from infection_monkey.i_puppet import PingScanData, PortScanData, PortStatus
from infection_monkey.master import Propagator

dot_1_results = (
    PingScanData(True, "windows"),
    {
        22: PortScanData(22, PortStatus.CLOSED, None, None),
        445: PortScanData(445, PortStatus.OPEN, "SMB BANNER", "tcp-445"),
        3389: PortScanData(3389, PortStatus.OPEN, "", "tcp-3389"),
    },
)

dot_3_results = (
    PingScanData(True, "linux"),
    {
        22: PortScanData(22, PortStatus.OPEN, "SSH BANNER", "tcp-22"),
        443: PortScanData(443, PortStatus.OPEN, "HTTPS BANNER", "tcp-443"),
        3389: PortScanData(3389, PortStatus.CLOSED, "", None),
    },
)

dead_host_results = (
    PingScanData(False, None),
    {
        22: PortScanData(22, PortStatus.CLOSED, None, None),
        443: PortScanData(443, PortStatus.CLOSED, None, None),
        3389: PortScanData(3389, PortStatus.CLOSED, "", None),
    },
)

dot_1_services = {
    "tcp-445": {"display_name": "unknown(TCP)", "port": 445, "banner": "SMB BANNER"},
    "tcp-3389": {"display_name": "unknown(TCP)", "port": 3389, "banner": ""},
}

dot_3_services = {
    "tcp-22": {"display_name": "unknown(TCP)", "port": 22, "banner": "SSH BANNER"},
    "tcp-443": {"display_name": "unknown(TCP)", "port": 443, "banner": "HTTPS BANNER"},
}


class MockIPScanner:
    def scan(self, ips_to_scan, options, results_callback, stop):
        for ip in ips_to_scan:
            if ip.endswith(".1"):
                results_callback(ip, *dot_1_results)
            elif ip.endswith(".3"):
                results_callback(ip, *dot_3_results)
            else:
                results_callback(ip, *dead_host_results)


def test_scan_result_processing(telemetry_messenger_spy):
    p = Propagator(telemetry_messenger_spy, MockIPScanner())
    p.propagate(
        {"targets": {"subnet_scan_list": ["10.0.0.1", "10.0.0.2", "10.0.0.3"]}, "network_scan": {}},
        Event(),
    )

    assert len(telemetry_messenger_spy.telemetries) == 3

    for t in telemetry_messenger_spy.telemetries:
        data = t.get_data()
        ip = data["machine"]["ip_addr"]

        if ip.endswith(".1"):
            assert data["service_count"] == 2
            assert data["machine"]["os"]["type"] == "windows"
            assert data["machine"]["services"] == dot_1_services
            assert data["machine"]["icmp"] is True
        elif ip.endswith(".3"):
            assert data["service_count"] == 2
            assert data["machine"]["os"]["type"] == "linux"
            assert data["machine"]["services"] == dot_3_services
            assert data["machine"]["icmp"] is True
        else:
            assert data["service_count"] == 0
            assert data["machine"]["os"] == {}
            assert data["machine"]["services"] == {}
            assert data["machine"]["icmp"] is False
