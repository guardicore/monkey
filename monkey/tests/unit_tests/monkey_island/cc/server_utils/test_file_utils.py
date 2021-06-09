import os
import subprocess

import pytest

from monkey_island.cc.server_utils import file_utils


def test_expand_user(patched_home_env):
    input_path = os.path.join("~", "test")
    expected_path = os.path.join(patched_home_env, "test")

    assert file_utils.expand_path(input_path) == expected_path


def test_expand_vars(patched_home_env):
    input_path = os.path.join("$HOME", "test")
    expected_path = os.path.join(patched_home_env, "test")

    assert file_utils.expand_path(input_path) == expected_path


@pytest.mark.skipif(os.name != "posix", reason="Tests Posix (not Windows) permissions.")
def test_has_expected_permissions_true_linux(tmpdir, create_empty_tmp_file):
    file_name = create_empty_tmp_file("test")
    os.chmod(file_name, 0o754)

    assert file_utils.has_expected_permissions(file_name, 0o754)


@pytest.mark.skipif(os.name != "posix", reason="Tests Posix (not Windows) permissions.")
def test_has_expected_permissions_false_linux(tmpdir, create_empty_tmp_file):
    file_name = create_empty_tmp_file("test")
    os.chmod(file_name, 0o755)

    assert not file_utils.has_expected_permissions(file_name, 0o700)


@pytest.mark.skipif(os.name == "posix", reason="Tests Windows (not Posix) permissions.")
def test_has_expected_permissions_true_windows(tmpdir, create_empty_tmp_file):
    file_name = create_empty_tmp_file("test")
    subprocess.run(f"echo y| cacls {file_name} /p %USERNAME%:F", shell=True)  # noqa: DUO116

    assert file_utils.has_expected_permissions(file_name, 2032127)


@pytest.mark.skipif(os.name == "posix", reason="Tests Windows (not Posix) permissions.")
def test_has_expected_permissions_false_windows(tmpdir, create_empty_tmp_file):
    file_name = create_empty_tmp_file("test")
    subprocess.run(f"echo y| cacls {file_name} /p %USERNAME%:R", shell=True)  # noqa: DUO116

    assert not file_utils.has_expected_permissions(file_name, 2032127)
