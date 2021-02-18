import pytest

from common.utils.attack_utils import ScanStatus
from infection_monkey.telemetry.attack.t1105_telem import T1105Telem


DST_IP = "0.0.0.1"
FILENAME = "virus.exe"
SRC_IP = "0.0.0.0"
STATUS = ScanStatus.USED


@pytest.fixture
def T1105_telem_test_instance():
    return T1105Telem(STATUS, SRC_IP, DST_IP, FILENAME)


def test_T1105_send(T1105_telem_test_instance, spy_send_telemetry):
    T1105_telem_test_instance.send()
    expected_data = {
        "status": STATUS.value,
        "technique": "T1105",
        "filename": FILENAME,
        "src": SRC_IP,
        "dst": DST_IP,
    }
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "attack"
