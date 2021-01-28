import subprocess

import pytest

from infection_monkey.utils.linux.users import AutoNewLinuxUser

TEST_USER = "test_user"


@pytest.fixture
def subprocess_check_output_spy(monkeypatch):
    def mock_check_output(command, stderr, shell):
        mock_check_output.command = command

    mock_check_output.command = ""

    monkeypatch.setattr(subprocess, "check_output", mock_check_output)

    return mock_check_output


def test_new_user_expires(subprocess_check_output_spy):
    with (AutoNewLinuxUser(TEST_USER, "password")):
        assert "--expiredate" in subprocess_check_output_spy.command
        assert "--inactive 0" in subprocess_check_output_spy.command


def test_new_user_try_delete(subprocess_check_output_spy):
    with (AutoNewLinuxUser(TEST_USER, "password")):
        pass
    assert f"deluser {TEST_USER}" in subprocess_check_output_spy.command
