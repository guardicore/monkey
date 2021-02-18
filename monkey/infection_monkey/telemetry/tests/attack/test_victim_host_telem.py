import pytest

from common.utils.attack_utils import ScanStatus, UsageEnum
from infection_monkey.model import VictimHost
from infection_monkey.telemetry.attack.victim_host_telem import VictimHostTelem


MACHINE = VictimHost('127.0.0.1')
STATUS = ScanStatus.USED
TECHNIQUE = 'T9999'


@pytest.fixture
def victim_host_telem_test_instance():
    return VictimHostTelem(TECHNIQUE, STATUS, MACHINE)


def test_victim_host_telem_send(victim_host_telem_test_instance, spy_send_telemetry):
    victim_host_telem_test_instance.send()
    expected_data = {'machine': {'domain_name': MACHINE.domain_name,
                                 'ip_addr': MACHINE.ip_addr},
                     'status': STATUS.value,
                     'technique': TECHNIQUE}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == 'attack'
