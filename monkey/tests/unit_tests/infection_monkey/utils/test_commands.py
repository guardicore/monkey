from ipaddress import IPv4Address
from uuid import UUID

import pytest

from common import OperatingSystem
from infection_monkey.i_puppet import TargetHost
from infection_monkey.utils.commands import (
    build_agent_download_command,
    build_monkey_commandline,
    build_monkey_commandline_parameters,
    get_monkey_commandline_linux,
    get_monkey_commandline_windows,
)
from infection_monkey.utils.ids import get_agent_id


@pytest.fixture
def agent_id():
    return get_agent_id()


def test_build_monkey_commandline_parameters_arguments():
    agent_id = UUID("9614480d-471b-4568-86b5-cb922a34ed8a")
    expected = [
        "-p",
        str(agent_id),
        "-s",
        "127.127.127.127:5000,138.138.138.138:5007",
        "-d",
        "0",
        "-l",
        "C:\\windows\\abc",
    ]
    actual = build_monkey_commandline_parameters(
        agent_id,
        ["127.127.127.127:5000", "138.138.138.138:5007"],
        0,
        "C:\\windows\\abc",
    )

    assert expected == actual


def test_build_monkey_commandline_parameters_depth_condition_greater():
    expected = [
        "-d",
        "50",
    ]
    actual = build_monkey_commandline_parameters(depth=50)

    assert expected == actual


def test_get_monkey_commandline_windows():
    expected = [
        "cmd.exe",
        "/c",
        "C:\\windows\\abc",
        "m0nk3y",
        "-p",
        "101010",
        "-s",
        "127.127.127.127:5000,138.138.138.138:5007",
    ]
    actual = get_monkey_commandline_windows(
        "C:\\windows\\abc",
        ["-p", "101010", "-s", "127.127.127.127:5000,138.138.138.138:5007"],
    )

    assert expected == actual


def test_get_monkey_commandline_linux():
    expected = [
        "/home/user/monkey-linux-64",
        "m0nk3y",
        "-p",
        "101010",
        "-s",
        "127.127.127.127:5000,138.138.138.138:5007",
    ]
    actual = get_monkey_commandline_linux(
        "/home/user/monkey-linux-64",
        ["-p", "101010", "-s", "127.127.127.127:5000,138.138.138.138:5007"],
    )

    assert expected == actual


def test_build_monkey_commandline(agent_id):
    servers = ["10.10.10.10:5000", "11.11.11.11:5007"]

    expected = f" -p {agent_id} -s 10.10.10.10:5000,11.11.11.11:5007 -d 0 -l /home/bla"
    actual = build_monkey_commandline(
        agent_id=agent_id, servers=servers, depth=0, location="/home/bla"
    )

    assert expected == actual


@pytest.mark.parametrize("servers", [None, []])
def test_build_monkey_commandline_empty_servers(agent_id, servers):
    expected = f" -p {agent_id} -d 0 -l /home/bla"
    actual = build_monkey_commandline(
        agent_id=agent_id, servers=servers, depth=0, location="/home/bla"
    )

    assert expected == actual


def test_build_agent_download_command__linux():
    target_host = TargetHost(ip=IPv4Address("1.1.1.1"), operating_system=OperatingSystem.LINUX)
    url = "https://example.com/agent"

    linux_agent_download_command = build_agent_download_command(target_host, url)

    assert linux_agent_download_command.startswith("wget")
    assert linux_agent_download_command.endswith(url)


def test_build_agent_download_command__windows():
    target_host = TargetHost(ip=IPv4Address("1.1.1.1"), operating_system=OperatingSystem.WINDOWS)
    url = "https://example.com/agent"

    with pytest.raises(NotImplementedError):
        build_agent_download_command(target_host, url)
