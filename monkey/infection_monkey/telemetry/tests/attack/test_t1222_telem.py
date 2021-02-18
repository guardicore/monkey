import pytest

from common.utils.attack_utils import ScanStatus
from infection_monkey.model import VictimHost
from infection_monkey.telemetry.attack.t1222_telem import T1222Telem


COMMAND = 'echo hi'
MACHINE = VictimHost('127.0.0.1')
STATUS = ScanStatus.USED


@pytest.fixture
def T1222_telem_test_instance():
    return T1222Telem(STATUS, COMMAND, MACHINE)


def test_T1222_send(T1222_telem_test_instance, spy_send_telemetry):
    T1222_telem_test_instance.send()
    expected_data = {'machine': {'domain_name': MACHINE.domain_name,
                                 'ip_addr': MACHINE.ip_addr},
                     'status': STATUS.value,
                     'technique': 'T1222',
                     'command': COMMAND}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == 'attack'
