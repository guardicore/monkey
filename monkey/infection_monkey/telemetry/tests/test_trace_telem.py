import json

import pytest

from infection_monkey.telemetry.trace_telem import TraceTelem


MSG = "message"


@pytest.fixture
def trace_telem_test_instance():
    return TraceTelem(MSG)


def test_trace_telem_send(trace_telem_test_instance, spy_send_telemetry):
    trace_telem_test_instance.send()
    expected_data = {"msg": MSG}
    expected_data = json.dumps(expected_data, cls=trace_telem_test_instance.json_encoder)

    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "trace"
