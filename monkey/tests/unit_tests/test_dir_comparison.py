from pathlib import Path

import pytest
from tests.utils import assert_directories_equal


@pytest.fixture
def directories_dir(data_for_tests_dir: Path) -> Path:
    return data_for_tests_dir / "dircmp"


@pytest.fixture
def dir1(directories_dir: Path) -> Path:
    return directories_dir / "dir1"


@pytest.fixture
def dir1_a(directories_dir: Path) -> Path:
    return directories_dir / "dir1_a"


def test_directories_equal(dir1: Path, dir1_a: Path):
    assert_directories_equal(dir1, dir1_a)


UNEQUAL_DIRS = ["dir1_recursive_2", "dir1_recursive_3", "dir2", "dir3", "dir4", "dir5"]


@pytest.mark.parametrize("dir2", UNEQUAL_DIRS)
def test_directories_not_equal(directories_dir, dir1: Path, dir2: str):
    with pytest.raises(AssertionError):
        assert_directories_equal(dir1, directories_dir / dir2)
