import filecmp

import pytest
from tests.utils import get_file_sha256_hash

from infection_monkey.payload.ransomware.readme_dropper import leave_readme

DEST_FILE = "README.TXT"
EMPTY_FILE_HASH = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


@pytest.fixture(scope="module")
def src_readme(data_for_tests_dir):
    return data_for_tests_dir / "test_readme.txt"


@pytest.fixture
def dest_readme(tmp_path):
    return tmp_path / DEST_FILE


@pytest.fixture
def expected_readme_windows(data_for_tests_dir):
    return data_for_tests_dir / "test_readme_windows.txt"


def test_readme_already_exists(src_readme, dest_readme):
    dest_readme.touch()

    leave_readme(src_readme, dest_readme)
    assert get_file_sha256_hash(dest_readme) == EMPTY_FILE_HASH


def test_leave_readme(src_readme, dest_readme):
    leave_readme(src_readme, dest_readme)
    assert filecmp.cmp(src_readme, dest_readme)


def test_leave_readme_windows(monkeypatch, src_readme, dest_readme, expected_readme_windows):
    leave_readme(src_readme, dest_readme)
    assert filecmp.cmp(dest_readme, expected_readme_windows)
