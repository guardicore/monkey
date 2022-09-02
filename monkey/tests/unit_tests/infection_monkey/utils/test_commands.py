import pytest

from infection_monkey.config import GUID
from infection_monkey.utils.commands import (
    build_monkey_commandline,
    build_monkey_commandline_explicitly,
    get_monkey_commandline_linux,
    get_monkey_commandline_windows,
)


def test_build_monkey_commandline_explicitly_arguments():
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
    actual = build_monkey_commandline_explicitly(
        "101010", ["127.127.127.127:5000", "138.138.138.138:5007"], 0, "C:\\windows\\abc"
    )

    assert expected == actual


def test_build_monkey_commandline_explicitly_depth_condition_greater():
    expected = [
        "-d",
        "50",
    ]
    actual = build_monkey_commandline_explicitly(depth=50)

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


def test_build_monkey_commandline():
    servers = ["10.10.10.10:5000", "11.11.11.11:5007"]

    expected = f" -p {GUID} -s 10.10.10.10:5000,11.11.11.11:5007 -d 0 -l /home/bla"
    actual = build_monkey_commandline(servers=servers, depth=0, location="/home/bla")

    assert expected == actual


@pytest.mark.parametrize("servers", [None, []])
def test_build_monkey_commandline_empty_servers(servers):

    expected = f" -p {GUID} -d 0 -l /home/bla"
    actual = build_monkey_commandline(servers, depth=0, location="/home/bla")

    assert expected == actual
