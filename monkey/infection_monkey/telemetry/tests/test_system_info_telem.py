import pytest

from infection_monkey.telemetry.system_info_telem import SystemInfoTelem


SYSTEM_INFO = {}


@pytest.fixture
def system_info_telem_test_instance():
    return SystemInfoTelem(SYSTEM_INFO)


def test_system_info_telem_send(system_info_telem_test_instance, spy_send_telemetry):
    system_info_telem_test_instance.send()
    expected_data = SYSTEM_INFO
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "system_info"
