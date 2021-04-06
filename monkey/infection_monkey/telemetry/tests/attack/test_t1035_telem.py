import json

import pytest

from common.utils.attack_utils import ScanStatus, UsageEnum
from infection_monkey.telemetry.attack.t1035_telem import T1035Telem


STATUS = ScanStatus.USED
USAGE = UsageEnum.SMB


@pytest.fixture
def T1035_telem_test_instance():
    return T1035Telem(STATUS, USAGE)


def test_T1035_send(T1035_telem_test_instance, spy_send_telemetry):
    T1035_telem_test_instance.send()
    expected_data = {"status": STATUS.value, "technique": "T1035", "usage": USAGE.name}
    expected_data = json.dumps(expected_data, cls=T1035_telem_test_instance.json_encoder)
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "attack"
