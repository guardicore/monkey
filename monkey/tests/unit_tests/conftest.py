import os
import sys
from pathlib import Path

import pytest

MONKEY_BASE_PATH = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, MONKEY_BASE_PATH)


@pytest.fixture(scope="session")
def data_for_tests_dir(pytestconfig):
    return Path(os.path.join(pytestconfig.rootdir, "monkey", "tests", "data_for_tests"))


@pytest.fixture(scope="session")
def stable_file(data_for_tests_dir) -> Path:
    return data_for_tests_dir / "stable_file.txt"


@pytest.fixture(scope="session")
def stable_file_sha256_hash() -> str:
    return "d9dcaadc91261692dafa86e7275b1bf39bb7e19d2efcfacd6fe2bfc9a1ae1062"


@pytest.fixture
def patched_home_env(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))

    return tmp_path
