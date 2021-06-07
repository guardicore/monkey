import os

import pytest


@pytest.fixture(scope="module")
def server_configs_dir(data_for_tests_dir):
    return os.path.join(data_for_tests_dir, "server_configs")


@pytest.fixture
def patched_home_env(monkeypatch, tmpdir):
    monkeypatch.setenv("HOME", str(tmpdir))

    return tmpdir


@pytest.fixture
def create_empty_file():
    def inner(file_name):
        with open(file_name, "w"):
            pass

    return inner
