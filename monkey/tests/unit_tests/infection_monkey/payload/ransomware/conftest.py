import shutil
from pathlib import Path

import pytest


@pytest.fixture
def patched_home_env(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))

    return tmp_path


@pytest.fixture(params=[".m0nk3y", ".test", ""], ids=["monkeyext", "testext", "noext"])
def ransomware_file_extension(request):
    return request.param


@pytest.fixture
def ransomware_test_data(data_for_tests_dir):
    return Path(data_for_tests_dir) / "ransomware_targets"


@pytest.fixture
def ransomware_target(tmp_path, ransomware_test_data):
    ransomware_target = tmp_path / "ransomware_target"
    shutil.copytree(ransomware_test_data, ransomware_target)

    return ransomware_target
