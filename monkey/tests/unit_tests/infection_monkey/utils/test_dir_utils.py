import os

import pytest
from tests.utils import is_user_admin

from infection_monkey.utils.dir_utils import (
    file_extension_filter,
    filter_files,
    get_all_regular_files_in_directory,
    is_not_symlink_filter,
)

FILES = ["file.jpg.zip", "file.xyz", "1.tar", "2.tgz", "2.png", "2.mpg"]
SUBDIRS = ["subdir1", "subdir2"]


def add_subdirs_to_dir(parent_dir):
    subdirs = [parent_dir / s for s in SUBDIRS]

    for subdir in subdirs:
        subdir.mkdir()

    return subdirs


def add_files_to_dir(parent_dir):
    files = [parent_dir / f for f in FILES]

    for f in files:
        f.touch()

    return files


def test_get_all_regular_files_in_directory__no_files(tmp_path, monkeypatch):
    add_subdirs_to_dir(tmp_path)

    expected_return_value = []
    assert get_all_regular_files_in_directory(tmp_path) == expected_return_value


def test_get_all_regular_files_in_directory__has_files(tmp_path, monkeypatch):
    add_subdirs_to_dir(tmp_path)
    files = add_files_to_dir(tmp_path)

    expected_return_value = sorted(files)
    assert sorted(get_all_regular_files_in_directory(tmp_path)) == expected_return_value


def test_get_all_regular_files_in_directory__subdir_has_files(tmp_path, monkeypatch):
    subdirs = add_subdirs_to_dir(tmp_path)
    add_files_to_dir(subdirs[0])

    files = add_files_to_dir(tmp_path)

    expected_return_value = sorted(files)
    assert sorted(get_all_regular_files_in_directory(tmp_path)) == expected_return_value


def test_filter_files__no_results(tmp_path):
    add_files_to_dir(tmp_path)

    files_in_dir = get_all_regular_files_in_directory(tmp_path)
    filtered_files = filter_files(files_in_dir, [lambda _: False])

    assert len(filtered_files) == 0


def test_filter_files__all_true(tmp_path):
    files = add_files_to_dir(tmp_path)
    expected_return_value = sorted(files)

    files_in_dir = get_all_regular_files_in_directory(tmp_path)
    filtered_files = filter_files(files_in_dir, [lambda _: True])

    assert sorted(filtered_files) == expected_return_value


def test_filter_files__multiple_filters(tmp_path):
    files = add_files_to_dir(tmp_path)
    expected_return_value = sorted(files[4:6])

    files_in_dir = get_all_regular_files_in_directory(tmp_path)
    filtered_files = filter_files(
        files_in_dir, [lambda f: f.name.startswith("2"), lambda f: f.name.endswith("g")]
    )

    assert sorted(filtered_files) == expected_return_value


def test_file_extension_filter(tmp_path):
    valid_extensions = {".zip", ".xyz"}

    files = add_files_to_dir(tmp_path)

    files_in_dir = get_all_regular_files_in_directory(tmp_path)
    filtered_files = filter_files(files_in_dir, [file_extension_filter(valid_extensions)])

    assert sorted(files[0:2]) == sorted(filtered_files)


@pytest.mark.skipif(
    os.name == "nt" and not is_user_admin(), reason="Test requires admin rights on Windows"
)
def test_is_not_symlink_filter(tmp_path):
    files = add_files_to_dir(tmp_path)
    link_path = tmp_path / "symlink.test"
    link_path.symlink_to(files[0], target_is_directory=False)

    files_in_dir = get_all_regular_files_in_directory(tmp_path)
    filtered_files = filter_files(files_in_dir, [is_not_symlink_filter])

    assert link_path in files_in_dir
    assert len(filtered_files) == len(FILES)
    assert link_path not in filtered_files
