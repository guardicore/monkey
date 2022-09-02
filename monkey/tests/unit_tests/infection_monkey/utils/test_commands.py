from infection_monkey.config import GUID
from infection_monkey.model.host import VictimHost
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
        "127.127.127.127:5000",
        "-d",
        "0",
        "-l",
        "C:\\windows\\abc",
    ]
    actual = build_monkey_commandline_explicitly(
        "101010", "127.127.127.127:5000", 0, "C:\\windows\\abc"
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
    ]
    actual = get_monkey_commandline_windows(
        "C:\\windows\\abc",
        [
            "-p",
            "101010",
        ],
    )

    assert expected == actual


def test_get_monkey_commandline_linux():
    expected = [
        "/home/user/monkey-linux-64",
        "m0nk3y",
        "-p",
        "101010",
    ]
    actual = get_monkey_commandline_linux(
        "/home/user/monkey-linux-64",
        [
            "-p",
            "101010",
        ],
    )

    assert expected == actual


def test_build_monkey_commandline():
    example_host = VictimHost(ip_addr="bla")
    example_host.set_island_address("101010", "5000")

    expected = f" -p {GUID} -s 101010:5000 -d 0 -l /home/bla"
    actual = build_monkey_commandline(target_host=example_host, depth=0, location="/home/bla")

    assert expected == actual
