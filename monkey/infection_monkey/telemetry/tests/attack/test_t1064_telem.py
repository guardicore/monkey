import json

import pytest

from common.utils.attack_utils import ScanStatus
from infection_monkey.telemetry.attack.t1064_telem import T1064Telem


STATUS = ScanStatus.USED
USAGE_STR = "[Usage info]"


@pytest.fixture
def T1064_telem_test_instance():
    return T1064Telem(STATUS, USAGE_STR)


def test_T1064_send(T1064_telem_test_instance, spy_send_telemetry):
    T1064_telem_test_instance.send()
    expected_data = {"status": STATUS.value, "technique": "T1064", "usage": USAGE_STR}
    expected_data = json.dumps(expected_data, cls=T1064_telem_test_instance.json_encoder)
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "attack"
