import json

import pytest

from infection_monkey.model.host import VictimHost
from infection_monkey.telemetry.scan_telem import ScanTelem

DOMAIN_NAME = "domain-name"
IP = "0.0.0.0"
HOST = VictimHost(IP, DOMAIN_NAME)
HOST_AS_DICT = {
    "ip_addr": IP,
    "domain_name": DOMAIN_NAME,
    "os": {},
    "services": {},
    "icmp": False,
    "default_server": None,
}
HOST_SERVICES = {}


@pytest.fixture
def scan_telem_test_instance():
    return ScanTelem(HOST)


def test_scan_telem_send(scan_telem_test_instance, spy_send_telemetry):
    scan_telem_test_instance.send()
    expected_data = {"machine": HOST_AS_DICT, "service_count": len(HOST_SERVICES)}
    expected_data = json.dumps(expected_data, cls=scan_telem_test_instance.json_encoder)

    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "scan"
