import pytest

from infection_monkey.utils.commands import (
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
    expected = [
        "-p",
        "101010",
        "-s",
        "127.127.127.127:5000,138.138.138.138:5007",
        "-d",
        "0",
        "-l",
        "C:\\windows\\abc",
    ]
    actual = build_monkey_commandline_parameters(
        "101010", ["127.127.127.127:5000", "138.138.138.138:5007"], 0, "C:\\windows\\abc"
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
