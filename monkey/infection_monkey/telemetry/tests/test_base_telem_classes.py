import pytest

from infection_monkey.exploit.wmiexec import WmiExploiter
from infection_monkey.model.host import VictimHost
from infection_monkey.post_breach.actions.schedule_jobs import ScheduleJobs
from infection_monkey.telemetry.exploit_telem import ExploitTelem
from infection_monkey.telemetry.post_breach_telem import PostBreachTelem
from infection_monkey.telemetry.scan_telem import ScanTelem
from infection_monkey.telemetry.state_telem import StateTelem
from infection_monkey.telemetry.system_info_telem import SystemInfoTelem
from infection_monkey.telemetry.trace_telem import TraceTelem
from infection_monkey.telemetry.tunnel_telem import TunnelTelem


DOMAIN_NAME = "domain-name"
HOSTNAME = "hostname"
IP = "0.0.0.0"
IS_DONE = True
MSG = "message"
RESULT = False
SYSTEM_INFO = {}
VERSION = "version"
HOST = VictimHost(IP, DOMAIN_NAME)
EXPLOITER = WmiExploiter(HOST)
PBA = ScheduleJobs()


@pytest.fixture
def exploit_telem_test_instance():
    return ExploitTelem(EXPLOITER, RESULT)


def test_exploit_telem_send(exploit_telem_test_instance, spy_send_telemetry):
    exploit_telem_test_instance.send()
    expected_data = {
        "result": RESULT,
        "machine": HOST.as_dict(),
        "exploiter": EXPLOITER.__class__.__name__,
        "info": EXPLOITER.exploit_info,
        "attempts": EXPLOITER.exploit_attempts,
    }
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "exploit"


@pytest.fixture
def post_breach_telem_test_instance(mocker):
    mocker.patch(
        "infection_monkey.telemetry.post_breach_telem.PostBreachTelem._get_hostname_and_ip",
        return_value=(HOSTNAME, IP),
    )
    return PostBreachTelem(PBA, RESULT)


def test_post_breach_telem_category(post_breach_telem_test_instance):
    assert post_breach_telem_test_instance.telem_category == "post_breach"


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


@pytest.fixture
def scan_telem_test_instance():
    return ScanTelem(HOST)


def test_scan_telem_send(scan_telem_test_instance, spy_send_telemetry):
    scan_telem_test_instance.send()
    expected_data = {"machine": HOST.as_dict(), "service_count": len(HOST.services)}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "scan"


@pytest.fixture
def state_telem_test_instance():
    return StateTelem(IS_DONE, VERSION)


def test_state_telem_send(state_telem_test_instance, spy_send_telemetry):
    state_telem_test_instance.send()
    expected_data = {"done": IS_DONE, "version": VERSION}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "state"


@pytest.fixture
def system_info_telem_test_instance():
    return SystemInfoTelem(SYSTEM_INFO)


def test_system_info_telem_send(system_info_telem_test_instance, spy_send_telemetry):
    system_info_telem_test_instance.send()
    expected_data = SYSTEM_INFO
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "system_info"


@pytest.fixture
def trace_telem_test_instance():
    return TraceTelem(MSG)


def test_trace_telem_send(trace_telem_test_instance, spy_send_telemetry):
    trace_telem_test_instance.send()
    expected_data = {"msg": MSG}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "trace"


@pytest.fixture
def tunnel_telem_test_instance():
    return TunnelTelem()


def test_tunnel_telem_send(tunnel_telem_test_instance, spy_send_telemetry):
    tunnel_telem_test_instance.send()
    expected_data = {"proxy": None}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "tunnel"
