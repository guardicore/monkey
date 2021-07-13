import pytest
from tests.utils import hash_file

from infection_monkey.ransomware.readme_utils import leave_readme

DEST_FILE = "README.TXT"
README_HASH = "c98c24b677eff44860afea6f493bbaec5bb1c4cbb209c6fc2bbb47f66ff2ad31"
EMPTY_FILE_HASH = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


@pytest.fixture(scope="module")
def src_readme(data_for_tests_dir):
    return data_for_tests_dir / "test_readme.txt"


@pytest.fixture
def dest_readme(tmp_path):
    return tmp_path / DEST_FILE


def test_readme_already_exists(src_readme, dest_readme):
    dest_readme.touch()

    leave_readme(src_readme, dest_readme)

    assert hash_file(dest_readme) == EMPTY_FILE_HASH


def test_leave_readme(src_readme, dest_readme):
    leave_readme(src_readme, dest_readme)

    assert hash_file(dest_readme) == README_HASH
