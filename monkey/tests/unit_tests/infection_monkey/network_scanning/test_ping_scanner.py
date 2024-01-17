import math
import subprocess
from unittest.mock import MagicMock

import pytest
from agentpluginapi import PingScanData
from monkeyevents import PingScanEvent
from monkeytypes import AgentID, OperatingSystem

import infection_monkey.network_scanning.ping_scanner  # noqa: F401
from infection_monkey.network_scanning import ping
from infection_monkey.network_scanning.ping_scanner import EMPTY_PING_SCAN

LINUX_SUCCESS_OUTPUT = """
PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.
64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=0.057 ms

--- 192.168.1.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.057/0.057/0.057/0.000 ms
"""

LINUX_NO_RESPONSE_OUTPUT = """
PING test-fake-domain.com (127.0.0.1) 56(84) bytes of data.

--- test-fake-domain.com ping statistics ---
1 packets transmitted, 0 received, 100% packet loss, time 0ms
"""

WINDOWS_SUCCESS_OUTPUT = """
Pinging 10.0.0.1 with 32 bytes of data:
Reply from 10.0.0.1: bytes=32 time=2ms TTL=127

Ping statistics for 10.0.0.1:
    Packets: Sent = 1, Received = 1, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 2ms, Maximum = 2ms, Average = 2ms
"""

WINDOWS_NO_RESPONSE_OUTPUT = """
Pinging 10.0.0.99 with 32 bytes of data:
Request timed out.

Ping statistics for 10.0.0.99:
    Packets: Sent = 1, Received = 0, Lost = 1 (100% loss),
"""

MALFORMED_OUTPUT = """
WUBBA LUBBA DUB DUBttl=1a1 time=0.201 ms
TTL=b10
TTL=1C
ttl=2d2!
"""


TIMESTAMP = 123.321
AGENT_ID = AgentID("a15111d3-e150-4ad5-a9b6-34f9d3a3105b")


@pytest.fixture(autouse=True)
def patch_timestamp(monkeypatch):
    monkeypatch.setattr("infection_monkey.network_scanning.ping_scanner.time", lambda: TIMESTAMP)


@pytest.fixture
def patch_subprocess_running_ping(monkeypatch):
    def inner(mock_obj):
        monkeypatch.setattr("subprocess.Popen", MagicMock(return_value=mock_obj))

    return inner


@pytest.fixture
def patch_subprocess_running_ping_with_ping_output(patch_subprocess_running_ping):
    def inner(ping_output):
        mock_ping = MagicMock()
        mock_ping.communicate = MagicMock(return_value=(ping_output, ""))
        patch_subprocess_running_ping(mock_ping)

    return inner


@pytest.fixture
def patch_subprocess_running_ping_to_raise_timeout_expired(patch_subprocess_running_ping):
    mock_ping = MagicMock()
    mock_ping.communicate = MagicMock(side_effect=subprocess.TimeoutExpired(["test-ping"], 10))

    patch_subprocess_running_ping(mock_ping)


@pytest.fixture
def set_os_linux(monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "Linux")


@pytest.fixture
def set_os_windows(monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "Windows")


HOST_IP = "192.168.1.1"
TIMEOUT = 1.0


def _get_ping_scan_event(result: PingScanData):
    return PingScanEvent(
        source=AGENT_ID,
        target=HOST_IP,
        timestamp=TIMESTAMP,
        tags=frozenset(),
        response_received=result.response_received,
        os=result.os,
    )


@pytest.mark.usefixtures("set_os_linux")
def test_linux_ping_success(patch_subprocess_running_ping_with_ping_output, mock_agent_event_queue):
    patch_subprocess_running_ping_with_ping_output(LINUX_SUCCESS_OUTPUT)
    result = ping(HOST_IP, TIMEOUT, mock_agent_event_queue, AGENT_ID)
    event = _get_ping_scan_event(result)

    assert result.response_received
    assert result.os == OperatingSystem.LINUX
    assert mock_agent_event_queue.publish.call_count == 1
    mock_agent_event_queue.publish.assert_called_with(event)


@pytest.mark.usefixtures("set_os_linux")
def test_linux_ping_no_response(
    patch_subprocess_running_ping_with_ping_output, mock_agent_event_queue
):
    patch_subprocess_running_ping_with_ping_output(LINUX_NO_RESPONSE_OUTPUT)
    result = ping(HOST_IP, TIMEOUT, mock_agent_event_queue, AGENT_ID)
    event = _get_ping_scan_event(result)

    assert not result.response_received
    assert result.os is None
    assert mock_agent_event_queue.publish.call_count == 1
    mock_agent_event_queue.publish.assert_called_with(event)


@pytest.mark.usefixtures("set_os_windows")
def test_windows_ping_success(
    patch_subprocess_running_ping_with_ping_output, mock_agent_event_queue
):
    patch_subprocess_running_ping_with_ping_output(WINDOWS_SUCCESS_OUTPUT)
    result = ping(HOST_IP, TIMEOUT, mock_agent_event_queue, AGENT_ID)
    event = _get_ping_scan_event(result)

    assert result.response_received
    assert result.os == OperatingSystem.WINDOWS
    assert mock_agent_event_queue.publish.call_count == 1
    mock_agent_event_queue.publish.assert_called_with(event)


@pytest.mark.usefixtures("set_os_windows")
def test_windows_ping_no_response(
    patch_subprocess_running_ping_with_ping_output, mock_agent_event_queue
):
    patch_subprocess_running_ping_with_ping_output(WINDOWS_NO_RESPONSE_OUTPUT)
    result = ping(HOST_IP, TIMEOUT, mock_agent_event_queue, AGENT_ID)
    event = _get_ping_scan_event(result)

    assert not result.response_received
    assert result.os is None
    assert mock_agent_event_queue.publish.call_count == 1
    mock_agent_event_queue.publish.assert_called_with(event)


def test_malformed_ping_command_response(
    patch_subprocess_running_ping_with_ping_output, mock_agent_event_queue
):
    patch_subprocess_running_ping_with_ping_output(MALFORMED_OUTPUT)
    result = ping(HOST_IP, TIMEOUT, mock_agent_event_queue, AGENT_ID)
    event = _get_ping_scan_event(result)

    assert not result.response_received
    assert result.os is None
    assert mock_agent_event_queue.publish.call_count == 1
    mock_agent_event_queue.publish.assert_called_with(event)


@pytest.mark.usefixtures("patch_subprocess_running_ping_to_raise_timeout_expired")
def test_timeout_expired(mock_agent_event_queue):
    result = ping(HOST_IP, TIMEOUT, mock_agent_event_queue, AGENT_ID)
    event = _get_ping_scan_event(result)

    assert not result.response_received
    assert result.os is None
    assert mock_agent_event_queue.publish.call_count == 1
    mock_agent_event_queue.publish.assert_called_with(event)


@pytest.fixture
def ping_command_spy(monkeypatch):
    ping_stub = MagicMock()
    monkeypatch.setattr("subprocess.Popen", ping_stub)

    return ping_stub


@pytest.fixture
def assert_expected_timeout(ping_command_spy, mock_agent_event_queue):
    def inner(timeout_flag, timeout_input, expected_timeout):
        ping(HOST_IP, timeout_input, mock_agent_event_queue, AGENT_ID)

        assert ping_command_spy.call_args is not None

        ping_command = ping_command_spy.call_args[0][0]
        assert timeout_flag in ping_command

        timeout_flag_index = ping_command.index(timeout_flag)
        assert ping_command[timeout_flag_index + 1] == expected_timeout

        assert mock_agent_event_queue.publish.call_count == 1

    return inner


@pytest.mark.usefixtures("set_os_windows")
def test_windows_timeout(assert_expected_timeout):
    timeout_flag = "-w"
    timeout = 1.42379

    assert_expected_timeout(timeout_flag, timeout, str(1423))


@pytest.mark.usefixtures("set_os_linux")
def test_linux_timeout(assert_expected_timeout):
    timeout_flag = "-W"
    timeout = 1.42379

    assert_expected_timeout(timeout_flag, timeout, str(math.ceil(timeout)))


def test_exception_handling(monkeypatch, mock_agent_event_queue):
    monkeypatch.setattr(
        "infection_monkey.network_scanning.ping_scanner._ping", MagicMock(side_effect=Exception)
    )
    assert ping("abc", 10, mock_agent_event_queue, AGENT_ID) == EMPTY_PING_SCAN
    assert mock_agent_event_queue.publish.call_count == 0
