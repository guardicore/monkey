from pathlib import Path
from typing import Callable, Optional
from unittest.mock import MagicMock

import pytest
from agent_plugins.payloads.ransomware.src import internal_ransomware_options
from agent_plugins.payloads.ransomware.src.internal_ransomware_options import (
    InternalRansomwareOptions,
)
from agent_plugins.payloads.ransomware.src.ransomware_options import RansomwareOptions
from monkeytypes import OperatingSystem
from tests.utils import raise_

from common.utils.environment import get_os
from common.utils.file_utils import InvalidPath

LINUX_DIR = "/tmp/test"
WINDOWS_DIR = "C:\\tmp\\test"

RANSOMWARE_OPTIONS_OBJECT = RansomwareOptions(
    file_extension=".encrypted",
    linux_target_dir=LINUX_DIR,
    windows_target_dir=WINDOWS_DIR,
    leave_readme=True,
)


@pytest.mark.parametrize("file_extension", (".xyz", ".m0nk3y"))
def test_file_extension(file_extension: str):
    internal_options = InternalRansomwareOptions(
        RansomwareOptions(file_extension=file_extension), MagicMock()
    )

    assert internal_options.file_extension == file_extension


@pytest.mark.parametrize("leave_readme", (True, False))
def test_leave_readme(leave_readme: bool):
    internal_options = InternalRansomwareOptions(
        RansomwareOptions(leave_readme=leave_readme), MagicMock()
    )

    assert internal_options.leave_readme == leave_readme


def test_linux_target_dir(monkeypatch: Callable):
    internal_options = InternalRansomwareOptions(RANSOMWARE_OPTIONS_OBJECT, OperatingSystem.LINUX)
    assert internal_options.target_directory == Path(LINUX_DIR)


def test_windows_target_dir(monkeypatch: Callable):
    internal_options = InternalRansomwareOptions(RANSOMWARE_OPTIONS_OBJECT, OperatingSystem.WINDOWS)
    assert internal_options.target_directory == Path(WINDOWS_DIR)


def test_env_variables_in_target_dir_resolved(home_env_variable: str, patched_home_env: str):
    path_with_env_variable = f"{home_env_variable}/ransomware_target"
    if get_os() == OperatingSystem.LINUX:
        options = RansomwareOptions(linux_target_dir=path_with_env_variable)
    else:
        options = RansomwareOptions(windows_target_dir=path_with_env_variable)

    internal_options = InternalRansomwareOptions(options, MagicMock())

    assert internal_options.target_directory == patched_home_env / "ransomware_target"


@pytest.mark.parametrize("target_dir", (None, ""))
def test_empty_target_dir(target_dir: Optional[str]):
    options = RansomwareOptions(linux_target_dir=target_dir, windows_target_dir=target_dir)

    internal_options = InternalRansomwareOptions(options, MagicMock())

    assert internal_options.target_directory is None


def test_invalid_target_dir(monkeypatch: Callable):
    monkeypatch.setattr(
        internal_ransomware_options, "expand_path", lambda _: raise_(InvalidPath("invalid"))
    )

    internal_options = InternalRansomwareOptions(RANSOMWARE_OPTIONS_OBJECT, MagicMock())

    assert internal_options.target_directory is None
