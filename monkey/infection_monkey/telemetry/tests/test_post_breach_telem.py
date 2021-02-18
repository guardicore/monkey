import pytest

from infection_monkey.post_breach.actions.schedule_jobs import ScheduleJobs
from infection_monkey.telemetry.post_breach_telem import PostBreachTelem


HOSTNAME = "hostname"
IP = "0.0.0.0"
PBA = ScheduleJobs()
RESULT = False


@pytest.fixture
def post_breach_telem_test_instance(monkeypatch):
    monkeypatch.setattr(PostBreachTelem, "_get_hostname_and_ip", lambda: (HOSTNAME, IP))
    return PostBreachTelem(PBA, RESULT)


def test_post_breach_telem_send(post_breach_telem_test_instance, spy_send_telemetry):
    post_breach_telem_test_instance.send()
    expected_data = {
        "command": PBA.command,
        "result": RESULT,
        "name": PBA.name,
        "hostname": HOSTNAME,
        "ip": IP,
    }
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "post_breach"
