import pytest

from infection_monkey.telemetry.post_breach_telem import PostBreachTelem


HOSTNAME = "hostname"
IP = "0.0.0.0"
PBA_COMMAND = "run some pba"
PBA_NAME = "some pba"
RESULT = False


class StubSomePBA:
    def __init__(self):
        self.name = PBA_NAME
        self.command = PBA_COMMAND


@pytest.fixture
def post_breach_telem_test_instance(monkeypatch):
    PBA = StubSomePBA()
    monkeypatch.setattr(PostBreachTelem, "_get_hostname_and_ip", lambda: (HOSTNAME, IP))
    return PostBreachTelem(PBA, RESULT)


def test_post_breach_telem_send(post_breach_telem_test_instance, spy_send_telemetry):
    post_breach_telem_test_instance.send()
    expected_data = {
        "command": PBA_COMMAND,
        "result": RESULT,
        "name": PBA_NAME,
        "hostname": HOSTNAME,
        "ip": IP,
    }
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "post_breach"
