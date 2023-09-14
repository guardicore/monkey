import filecmp
from pathlib import Path

import pytest
from agent_plugins.payloads.ransomware.src.readme_dropper import ReadmeDropper
from tests.utils import get_file_sha256_hash

from common import OperatingSystem

DEST_FILE = "README.TXT"
EMPTY_FILE_HASH = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
WINDOWS_README_FILE_HASH = "4231329e0212592178f9d590cdc0cfcf4dc691b135e2cb4fc49227b17d32ca8c"


@pytest.fixture(scope="module")
def src_readme(data_for_tests_dir: Path) -> Path:
    return data_for_tests_dir / "test_readme.txt"


@pytest.fixture
def dest_readme(tmp_path: Path) -> Path:
    return tmp_path / DEST_FILE


def test_readme_already_exists(src_readme: Path, dest_readme: Path):
    readme_dropper = ReadmeDropper(OperatingSystem.LINUX)
    dest_readme.touch()

    readme_dropper.leave_readme(src_readme, dest_readme)

    assert get_file_sha256_hash(dest_readme) == EMPTY_FILE_HASH


def test_leave_readme_linux(src_readme: Path, dest_readme: Path):
    readme_dropper = ReadmeDropper(OperatingSystem.LINUX)

    readme_dropper.leave_readme(src_readme, dest_readme)

    assert filecmp.cmp(src_readme, dest_readme)


def test_leave_readme_windows(src_readme: Path, dest_readme: Path):
    readme_dropper = ReadmeDropper(OperatingSystem.WINDOWS)

    readme_dropper.leave_readme(src_readme, dest_readme)

    assert get_file_sha256_hash(dest_readme) == WINDOWS_README_FILE_HASH
