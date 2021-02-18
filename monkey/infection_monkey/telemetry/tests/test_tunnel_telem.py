import pytest

from infection_monkey.telemetry.tunnel_telem import TunnelTelem


@pytest.fixture
def tunnel_telem_test_instance():
    return TunnelTelem()


def test_tunnel_telem_send(tunnel_telem_test_instance, spy_send_telemetry):
    tunnel_telem_test_instance.send()
    expected_data = {"proxy": None}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "tunnel"
