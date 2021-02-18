import pytest

from common.utils.attack_utils import ScanStatus
from infection_monkey.telemetry.attack.t1107_telem import T1107Telem


PATH = 'path/to/file.txt'
STATUS = ScanStatus.USED


@pytest.fixture
def T1107_telem_test_instance():
    return T1107Telem(STATUS, PATH)


def test_T1107_send(T1107_telem_test_instance, spy_send_telemetry):
    T1107_telem_test_instance.send()
    expected_data = {'status': STATUS.value,
                     'technique': 'T1107',
                     'path': PATH}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == 'attack'
