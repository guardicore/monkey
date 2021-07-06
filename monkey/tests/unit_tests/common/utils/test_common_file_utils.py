import os

from common.utils.file_utils import expand_path


def test_expand_user(patched_home_env):
    input_path = os.path.join("~", "test")
    expected_path = os.path.join(patched_home_env, "test")

    assert expand_path(input_path) == expected_path


def test_expand_vars(patched_home_env):
    input_path = os.path.join("$HOME", "test")
    expected_path = os.path.join(patched_home_env, "test")

    assert expand_path(input_path) == expected_path
