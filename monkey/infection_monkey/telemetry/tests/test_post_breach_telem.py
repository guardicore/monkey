import pytest

from common.data.post_breach_consts import POST_BREACH_JOB_SCHEDULING
from infection_monkey.post_breach.actions.schedule_jobs import ScheduleJobs
from infection_monkey.post_breach.job_scheduling.linux_job_scheduling import \
    get_linux_commands_to_schedule_jobs
from infection_monkey.post_breach.job_scheduling.windows_job_scheduling import \
    get_windows_commands_to_schedule_jobs
from infection_monkey.telemetry.post_breach_telem import PostBreachTelem
from infection_monkey.utils.environment import is_windows_os


HOSTNAME = "hostname"
IP = "0.0.0.0"
PBA = ScheduleJobs()
PBA_COMMAND = get_windows_commands_to_schedule_jobs() if is_windows_os() else\
     ' '.join(get_linux_commands_to_schedule_jobs())
PBA_NAME = POST_BREACH_JOB_SCHEDULING
RESULT = False


@pytest.fixture
def post_breach_telem_test_instance(monkeypatch):
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
