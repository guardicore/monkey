import pytest

from infection_monkey.telemetry.trace_telem import TraceTelem

MSG = "message"


@pytest.fixture
def trace_telem_test_instance():
    return TraceTelem(MSG)


def test_trace_telem_send(trace_telem_test_instance, spy_send_telemetry):
    trace_telem_test_instance.send()
    expected_data = {"msg": MSG}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "trace"
