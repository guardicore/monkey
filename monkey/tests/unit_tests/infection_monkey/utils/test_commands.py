from infection_monkey.utils.commands import (
    build_monkey_commandline_explicitly,
    get_monkey_commandline_linux,
    get_monkey_commandline_windows,
)


def test_build_monkey_commandline_explicitly_arguments():
    expected = [
        "-p",
        "101010",
        "-t",
        "10.10.101.10",
        "-s",
        "127.127.127.127:5000",
        "-d",
        "0",
        "-l",
        "C:\\windows\\abc",
        "-vp",
        "80",
    ]
    actual = build_monkey_commandline_explicitly(
        101010, "10.10.101.10", "127.127.127.127:5000", 0, "C:\\windows\\abc", 80
    )

    assert expected == actual


def test_build_monkey_commandline_explicitly_depth_condition_less():
    expected = [
        "-d",
        "0",
    ]
    actual = build_monkey_commandline_explicitly(depth=-50)

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
        "-t",
        "10.10.101.10",
    ]
    actual = get_monkey_commandline_windows(
        "C:\\windows\\abc",
        [
            "-p",
            "101010",
            "-t",
            "10.10.101.10",
        ],
    )

    assert expected == actual


def test_get_monkey_commandline_linux():
    expected = [
        "monkey-linux-64",
        "m0nk3y",
        "-p",
        "101010",
        "-t",
        "10.10.101.10",
    ]
    actual = get_monkey_commandline_linux(
        "/home/user/monkey-linux-64",
        [
            "-p",
            "101010",
            "-t",
            "10.10.101.10",
        ],
    )

    assert expected == actual
