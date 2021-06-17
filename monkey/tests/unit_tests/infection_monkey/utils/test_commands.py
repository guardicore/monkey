from infection_monkey.utils.commands import build_monkey_commandline_explicitly


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

    assert test1 == result1
