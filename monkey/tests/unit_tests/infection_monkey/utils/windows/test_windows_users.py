import os
import subprocess

import pytest

from infection_monkey.utils.windows.users import AutoNewWindowsUser

TEST_USER = "test_user"


@pytest.fixture
def subprocess_check_output_spy(monkeypatch):
    def mock_check_output(command, stderr, timeout):
        mock_check_output.command = command

    mock_check_output.command = ""

    monkeypatch.setattr(subprocess, "check_output", mock_check_output)

    return mock_check_output


class StubLogonUser:
    def __init__(self):
        pass

    def Close():
        return None


@pytest.mark.skipif(os.name == "posix", reason="This test only runs on Windows.")
def test_new_user_delete_windows(subprocess_check_output_spy, monkeypatch):
    monkeypatch.setattr(
        "infection_monkey.utils.windows.users.win32security.LogonUser",
        lambda _, __, ___, ____, _____: StubLogonUser,
    )

    with (AutoNewWindowsUser(TEST_USER, "password")):
        pass

    assert f"net user {TEST_USER} /delete" in " ".join(subprocess_check_output_spy.command)
