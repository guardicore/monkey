import json

import pytest

from common.utils.attack_utils import ScanStatus
from infection_monkey.telemetry.attack.t1145_telem import T1145Telem

NAME = "ubuntu"
HOME_DIR = "/home/ubuntu"
STATUS = ScanStatus.USED


@pytest.fixture
def T1145_telem_test_instance():
    return T1145Telem(STATUS, NAME, HOME_DIR)


def test_T1145_send(T1145_telem_test_instance, spy_send_telemetry):
    T1145_telem_test_instance.send()
    expected_data = {
        "status": STATUS.value,
        "technique": "T1145",
        "name": NAME,
        "home_dir": HOME_DIR,
    }
    expected_data = json.dumps(expected_data, cls=T1145_telem_test_instance.json_encoder)
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "attack"
