import os

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
def test_has_expected_permissions_true(tmpdir):
    file_name = f"{tmpdir}/test"

    create_empty_file(file_name)
    os.chmod(file_name, 0o754)

    assert file_utils.has_expected_permissions(file_name, 0o754)


@pytest.mark.skipif(os.name != "posix", reason="Tests Posix (not Windows) permissions.")
def test_has_expected_permissions_false(tmpdir):
    file_name = f"{tmpdir}/test"

    create_empty_file(file_name)
    os.chmod(file_name, 0o755)

    assert not file_utils.has_expected_permissions(file_name, 0o700)


def create_empty_file(file_name):
    with open(file_name, "w"):
        pass
