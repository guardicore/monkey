from pathlib import Path

import pytest
from tests.utils import raise_

from common.utils.file_utils import InvalidPath
from infection_monkey.payload.ransomware import ransomware_options
from infection_monkey.payload.ransomware.ransomware_options import (
    EncryptionAlgorithm,
    RansomwareOptions,
)

EXTENSION = ".testext"
LINUX_DIR = "/tmp/test"
WINDOWS_DIR = "C:\\tmp\\test"
ALGORITHM = str(EncryptionAlgorithm.BIT_FLIP)


@pytest.fixture
def options_from_island():
    return {
        "encryption": {
            "enabled": None,
            "file_extension": EXTENSION,
            "directories": {
                "linux_target_dir": LINUX_DIR,
                "windows_target_dir": WINDOWS_DIR,
            },
            "algorithm": ALGORITHM,
            "recursive": False,
        },
        "other_behaviors": {"readme": None},
    }


@pytest.mark.parametrize("enabled", [True, False])
def test_encryption_enabled(enabled, options_from_island):
    options_from_island["encryption"]["enabled"] = enabled
    options = RansomwareOptions(options_from_island)

    assert options.encryption_enabled == enabled


@pytest.mark.parametrize("enabled", [True, False])
def test_readme_enabled(enabled, options_from_island):
    options_from_island["other_behaviors"]["readme"] = enabled
    options = RansomwareOptions(options_from_island)

    assert options.readme_enabled == enabled


def test_file_extension(options_from_island):
    options = RansomwareOptions(options_from_island)

    assert options.file_extension == EXTENSION


def test_empty_file_extension(options_from_island):
    options_from_island["encryption"]["file_extension"] = ""
    options = RansomwareOptions(options_from_island)

    assert options.file_extension == ""


@pytest.mark.parametrize("invalid_extension", ["test", "test.", ".te\\st", ".test/", ".test/test"])
def test_invalid_file_extension(options_from_island, invalid_extension: str):
    options_from_island["encryption"]["file_extension"] = invalid_extension

    with pytest.raises(ValueError):
        RansomwareOptions(options_from_island)


def test_linux_target_dir(monkeypatch, options_from_island):
    monkeypatch.setattr(ransomware_options, "is_windows_os", lambda: False)

    options = RansomwareOptions(options_from_island)
    assert options.target_directory == Path(LINUX_DIR)


def test_windows_target_dir(monkeypatch, options_from_island):
    monkeypatch.setattr(ransomware_options, "is_windows_os", lambda: True)

    options = RansomwareOptions(options_from_island)
    assert options.target_directory == Path(WINDOWS_DIR)


def test_env_variables_in_target_dir_resolved(
    options_from_island, home_env_variable, patched_home_env, tmp_path
):
    path_with_env_variable = f"{home_env_variable}/ransomware_target"

    options_from_island["encryption"]["directories"]["linux_target_dir"] = options_from_island[
        "encryption"
    ]["directories"]["windows_target_dir"] = path_with_env_variable

    options = RansomwareOptions(options_from_island)
    assert options.target_directory == patched_home_env / "ransomware_target"


def test_target_dir_is_none(monkeypatch, options_from_island):
    monkeypatch.setattr(ransomware_options, "expand_path", lambda _: raise_(InvalidPath("invalid")))

    options = RansomwareOptions(options_from_island)
    assert options.target_directory is None


@pytest.mark.parametrize("algorithm", [a for a in EncryptionAlgorithm])
def test_valid_encryption_algorithms(options_from_island, algorithm: EncryptionAlgorithm):
    options_from_island["encryption"]["algorithm"] = algorithm

    options = RansomwareOptions(options_from_island)

    assert options.algorithm == algorithm


def test_invalid_encryption_algorithms(options_from_island):
    options_from_island["encryption"]["algorithm"] = "invalid_algorithm"

    with pytest.raises(ValueError):
        RansomwareOptions(options_from_island)


@pytest.mark.parametrize("recursive", [True, False])
def test_recursive(options_from_island, recursive: bool):
    options_from_island["encryption"]["recursive"] = recursive

    options = RansomwareOptions(options_from_island)
    assert options.recursive is recursive
