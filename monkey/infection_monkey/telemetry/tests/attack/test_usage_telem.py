import pytest

from common.utils.attack_utils import ScanStatus, UsageEnum
from infection_monkey.telemetry.attack.usage_telem import UsageTelem


STATUS = ScanStatus.USED
TECHNIQUE = 'T9999'
USAGE = UsageEnum.SMB


@pytest.fixture
def usage_telem_test_instance():
    return UsageTelem(TECHNIQUE, STATUS, USAGE)


def test_usage_telem_send(usage_telem_test_instance, spy_send_telemetry):
    usage_telem_test_instance.send()
    expected_data = {'status': STATUS.value,
                     'technique': TECHNIQUE,
                     'usage': USAGE.name}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == 'attack'
