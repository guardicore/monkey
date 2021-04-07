import json

import pytest

from common.utils.attack_utils import ScanStatus
from infection_monkey.model import VictimHost
from infection_monkey.telemetry.attack.victim_host_telem import VictimHostTelem

DOMAIN_NAME = "domain-name"
IP = "127.0.0.1"
MACHINE = VictimHost(IP, DOMAIN_NAME)
STATUS = ScanStatus.USED
TECHNIQUE = "T9999"


@pytest.fixture
def victim_host_telem_test_instance():
    return VictimHostTelem(TECHNIQUE, STATUS, MACHINE)


def test_victim_host_telem_send(victim_host_telem_test_instance, spy_send_telemetry):
    victim_host_telem_test_instance.send()
    expected_data = {
        "status": STATUS.value,
        "technique": TECHNIQUE,
        "machine": {"domain_name": DOMAIN_NAME, "ip_addr": IP},
    }
    expected_data = json.dumps(expected_data, cls=victim_host_telem_test_instance.json_encoder)
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "attack"
