import json

import pytest

from infection_monkey.telemetry.tunnel_telem import TunnelTelem


@pytest.fixture
def tunnel_telem_test_instance():
    return TunnelTelem()


def test_tunnel_telem_send(tunnel_telem_test_instance, spy_send_telemetry):
    tunnel_telem_test_instance.send()
    expected_data = {"proxy": None}
    expected_data = json.dumps(expected_data, cls=tunnel_telem_test_instance.json_encoder)

    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "tunnel"
