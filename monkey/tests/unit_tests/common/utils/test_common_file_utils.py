import os

import pytest

from common.utils.file_utils import InvalidPath, expand_path


def test_expand_user(patched_home_env):
    input_path = os.path.join("~", "test")
    expected_path = os.path.join(patched_home_env, "test")

    assert expand_path(input_path) == expected_path


def test_expand_vars(patched_home_env):
    input_path = os.path.join("$HOME", "test")
    expected_path = os.path.join(patched_home_env, "test")

    assert expand_path(input_path) == expected_path


def test_expand_path__empty_path_provided():
    with pytest.raises(InvalidPath):
        expand_path("")
