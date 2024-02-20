from infection_monkey.utils.commands import (
    get_monkey_commandline_linux,
    get_monkey_commandline_windows,
)


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
