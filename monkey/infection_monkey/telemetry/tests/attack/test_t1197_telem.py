import pytest

from common.utils.attack_utils import ScanStatus
from infection_monkey.model import VictimHost
from infection_monkey.telemetry.attack.t1197_telem import T1197Telem


DOMAIN_NAME = 'domain-name'
IP = '127.0.0.1'
MACHINE = VictimHost(IP, DOMAIN_NAME)
STATUS = ScanStatus.USED
USAGE_STR = '[Usage info]'


@pytest.fixture
def T1197_telem_test_instance():
    return T1197Telem(STATUS, MACHINE, USAGE_STR)


def test_T1197_send(T1197_telem_test_instance, spy_send_telemetry):
    T1197_telem_test_instance.send()
    expected_data = {'machine': {'domain_name': DOMAIN_NAME,
                                 'ip_addr': IP},
                     'status': STATUS.value,
                     'technique': 'T1197',
                     'usage': USAGE_STR}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == 'attack'
