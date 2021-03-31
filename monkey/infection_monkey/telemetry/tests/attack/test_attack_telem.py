import json

import pytest

from common.utils.attack_utils import ScanStatus
from infection_monkey.telemetry.attack.attack_telem import AttackTelem


STATUS = ScanStatus.USED
TECHNIQUE = "T9999"


@pytest.fixture
def attack_telem_test_instance():
    return AttackTelem(TECHNIQUE, STATUS)


def test_attack_telem_send(attack_telem_test_instance, spy_send_telemetry):
    attack_telem_test_instance.send()
    expected_data = {"status": STATUS.value, "technique": TECHNIQUE}
    expected_data = json.dumps(expected_data, cls=attack_telem_test_instance.json_encoder)

    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "attack"
