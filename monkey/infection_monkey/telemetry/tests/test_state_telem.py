import pytest

from infection_monkey.telemetry.state_telem import StateTelem


IS_DONE = True
VERSION = "version"


@pytest.fixture
def state_telem_test_instance():
    return StateTelem(IS_DONE, VERSION)


def test_state_telem_send(state_telem_test_instance, spy_send_telemetry):
    state_telem_test_instance.send()
    expected_data = {"done": IS_DONE, "version": VERSION}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "state"
