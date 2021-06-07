import os

import pytest


@pytest.fixture(scope="module")
def server_configs_dir(data_for_tests_dir):
    return os.path.join(data_for_tests_dir, "server_configs")


@pytest.fixture
def patched_home_env(monkeypatch, tmpdir):
    monkeypatch.setenv("HOME", str(tmpdir))

    return tmpdir
