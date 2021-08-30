import subprocess

import pytest

from infection_monkey.utils.windows.users import AutoNewWindowsUser

TEST_USER = "test_user"
ACTIVE_NO_NET_USER = "/ACTIVE:NO"


@pytest.fixture
def subprocess_check_output_spy(monkeypatch):
    def mock_check_output(command, stderr):
        mock_check_output.command = command

    mock_check_output.command = ""

    monkeypatch.setattr(subprocess, "check_output", mock_check_output)

    return mock_check_output


def test_new_user_try_delete_windows(subprocess_check_output_spy):
    new_user = AutoNewWindowsUser(TEST_USER, "password")

    new_user.try_deactivate_user()
    assert f"net user {TEST_USER} {ACTIVE_NO_NET_USER}" in " ".join(
        subprocess_check_output_spy.command
    )

    new_user.try_delete_user()
    assert f"net user {TEST_USER} /delete" in " ".join(subprocess_check_output_spy.command)
