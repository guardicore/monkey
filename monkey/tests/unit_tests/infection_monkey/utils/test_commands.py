from infection_monkey.utils.commands import (
    build_monkey_commandline_explicitly,
    get_monkey_cmd_lines_windows,
)


def test_build_monkey_commandline_explicitly():
    test1 = [
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
    result1 = build_monkey_commandline_explicitly(
        101010, "10.10.101.10", "127.127.127.127:5000", 0, "C:\\windows\\abc", 80
    )

    test2 = [
        "-p",
        "101010",
        "-t",
        "10.10.101.10",
        "-s",
        "200.150.100.50:5000",
        "-d",
        "0",
        "-l",
        "C:\\windows\\abc",
        "-vp",
        "443",
    ]
    result2 = build_monkey_commandline_explicitly(
        101010, "10.10.101.10", "200.150.100.50:5000", -50, "C:\\windows\\abc", 443
    )

    test3 = [
        "-p",
        "101010",
        "-t",
        "10.10.101.10",
        "-s",
        "200.150.100.50:5000",
        "-d",
        "100",
        "-l",
        "C:\\windows\\ghi",
        "-vp",
        "443",
    ]
    result3 = build_monkey_commandline_explicitly(
        101010, "10.10.101.10", "200.150.100.50:5000", 100, "C:\\windows\\ghi", 443
    )

    assert test1 == result1
    assert test2 == result2
    assert test3 == result3


def test_get_monkey_cmd_lines_windows():
    test1 = [
        "cmd.exe",
        "/c",
        "C:\\windows\\abc",
        "m0nk3y",
        "-p",
        "101010",
        "-t",
        "10.10.101.10",
    ]
    result1 = get_monkey_cmd_lines_windows(
        "C:\\windows\\abc",
        [
            "-p",
            "101010",
            "-t",
            "10.10.101.10",
        ],
    )

    assert test1 == result1
