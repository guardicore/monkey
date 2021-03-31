import json

import pytest

from common.utils.attack_utils import ScanStatus, UsageEnum
from infection_monkey.telemetry.attack.t1129_telem import T1129Telem


STATUS = ScanStatus.USED
USAGE = UsageEnum.SMB


@pytest.fixture
def T1129_telem_test_instance():
    return T1129Telem(STATUS, USAGE)


def test_T1129_send(T1129_telem_test_instance, spy_send_telemetry):
    T1129_telem_test_instance.send()
    expected_data = {"status": STATUS.value, "technique": "T1129", "usage": USAGE.name}
    expected_data = json.dumps(expected_data, cls=T1129_telem_test_instance.json_encoder)
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "attack"
