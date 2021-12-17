from pathlib import Path

import pytest
from tests.utils import raise_

from common.utils.file_utils import InvalidPath
from infection_monkey.payload.ransomware import ransomware_config
from infection_monkey.payload.ransomware.ransomware_config import RansomwareConfig

LINUX_DIR = "/tmp/test"
WINDOWS_DIR = "C:\\tmp\\test"


@pytest.fixture
def config_from_island():
    return {
        "encryption": {
            "enabled": None,
            "directories": {
                "linux_target_dir": LINUX_DIR,
                "windows_target_dir": WINDOWS_DIR,
            },
        },
        "other_behaviors": {"readme": None},
    }


@pytest.mark.parametrize("enabled", [True, False])
def test_encryption_enabled(enabled, config_from_island):
    config_from_island["encryption"]["enabled"] = enabled
    config = RansomwareConfig(config_from_island)

    assert config.encryption_enabled == enabled


@pytest.mark.parametrize("enabled", [True, False])
def test_readme_enabled(enabled, config_from_island):
    config_from_island["other_behaviors"]["readme"] = enabled
    config = RansomwareConfig(config_from_island)

    assert config.readme_enabled == enabled


def test_linux_target_dir(monkeypatch, config_from_island):
    monkeypatch.setattr(ransomware_config, "is_windows_os", lambda: False)

    config = RansomwareConfig(config_from_island)
    assert config.target_directory == Path(LINUX_DIR)


def test_windows_target_dir(monkeypatch, config_from_island):
    monkeypatch.setattr(ransomware_config, "is_windows_os", lambda: True)

    config = RansomwareConfig(config_from_island)
    assert config.target_directory == Path(WINDOWS_DIR)


def test_env_variables_in_target_dir_resolved(config_from_island, patched_home_env, tmp_path):
    path_with_env_variable = "$HOME/ransomware_target"

    config_from_island["encryption"]["directories"]["linux_target_dir"] = config_from_island[
        "encryption"
    ]["directories"]["windows_target_dir"] = path_with_env_variable

    config = RansomwareConfig(config_from_island)
    assert config.target_directory == patched_home_env / "ransomware_target"


def test_target_dir_is_none(monkeypatch, config_from_island):
    monkeypatch.setattr(ransomware_config, "expand_path", lambda _: raise_(InvalidPath("invalid")))

    config = RansomwareConfig(config_from_island)
    assert config.target_directory is None
