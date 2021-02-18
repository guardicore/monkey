import pytest

from common.utils.attack_utils import ScanStatus, UsageEnum
from infection_monkey.telemetry.attack.t1106_telem import T1106Telem


STATUS = ScanStatus.USED
USAGE = UsageEnum.SMB


@pytest.fixture
def T1106_telem_test_instance():
    return T1106Telem(STATUS, USAGE)


def test_T1106_send(T1106_telem_test_instance, spy_send_telemetry):
    T1106_telem_test_instance.send()
    expected_data = {'status': STATUS.value,
                     'technique': 'T1106',
                     'usage': USAGE.name}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == 'attack'
