import json
from pathlib import Path

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


@pytest.mark.parametrize("filename", [Path(FILENAME), FILENAME])
def test_T1105_send(T1105_telem_test_instance, spy_send_telemetry, filename):
    T1105_telem_test_instance.send()
    expected_data = {
        "status": STATUS.value,
        "technique": "T1105",
        "filename": FILENAME,
        "src": SRC_IP,
        "dst": DST_IP,
    }
    expected_data = json.dumps(expected_data, cls=T1105_telem_test_instance.json_encoder)
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "attack"
