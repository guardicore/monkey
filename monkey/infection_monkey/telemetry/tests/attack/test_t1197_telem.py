import pytest

from common.utils.attack_utils import ScanStatus
from infection_monkey.model import VictimHost
from infection_monkey.telemetry.attack.t1197_telem import T1197Telem


MACHINE = VictimHost('127.0.0.1')
STATUS = ScanStatus.USED
USAGE_STR = '[Usage info]'


@pytest.fixture
def T1197_telem_test_instance():
    return T1197Telem(STATUS, MACHINE, USAGE_STR)


def test_T1197_send(T1197_telem_test_instance, spy_send_telemetry):
    T1197_telem_test_instance.send()
    expected_data = {'machine': {'domain_name': MACHINE.domain_name,
                                 'ip_addr': MACHINE.ip_addr},
                     'status': STATUS.value,
                     'technique': 'T1197',
                     'usage': USAGE_STR}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == 'attack'
