import os
import sys
from pathlib import Path

import pytest

MONKEY_BASE_PATH = str(Path(__file__).parent.parent)
sys.path.insert(0, MONKEY_BASE_PATH)


@pytest.fixture(scope="session")
def mocked_data_dir(pytestconfig):
    return os.path.join(pytestconfig.rootdir, "monkey", "tests", "mocked_data")


@pytest.fixture
def mock_home_env(monkeypatch, tmpdir):
    monkeypatch.setenv("HOME", str(tmpdir))

    return tmpdir
