import json

import pytest

from infection_monkey.telemetry.ransomware_telem import RansomwareTelem

ATTEMPTS = [("<file>", "<encryption attempt result>")]


@pytest.fixture
def ransomware_telem_test_instance():
    return RansomwareTelem(ATTEMPTS)


def test_ransomware_telem_send(ransomware_telem_test_instance, spy_send_telemetry):
    ransomware_telem_test_instance.send()
    expected_data = {"ransomware_attempts": ATTEMPTS}
    expected_data = json.dumps(expected_data, cls=ransomware_telem_test_instance.json_encoder)
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "ransomware"
