import pytest

from common.utils.attack_utils import ScanStatus
from infection_monkey.telemetry.attack.t1005_telem import T1005Telem


GATHERED_DATA_TYPE = '[Type of data collected]'
INFO = '[Additional info]'
STATUS = ScanStatus.USED


@pytest.fixture
def T1005_telem_test_instance():
    return T1005Telem(STATUS, GATHERED_DATA_TYPE, INFO)


def test_T1005_send(T1005_telem_test_instance, spy_send_telemetry):
    T1005_telem_test_instance.send()
    expected_data = {'status': STATUS.value,
                     'technique': 'T1005',
                     'gathered_data_type': GATHERED_DATA_TYPE,
                     'info': INFO}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == 'attack'
