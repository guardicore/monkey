import os

import pytest
from monkeytoolbox import get_all_regular_files_in_directory
from tests.utils import add_files_to_dir, is_user_admin

from infection_monkey.utils.file_utils import (
    file_extension_filter,
    filter_files,
    is_not_shortcut_filter,
    is_not_symlink_filter,
)

SHORTCUT = "shortcut.lnk"
FILES = ["file.jpg.zip", "file.xyz", "1.tar", "2.tgz", "2.png", "2.mpg", SHORTCUT]


def test_filter_files__no_results(tmp_path):
    add_files_to_dir(tmp_path, FILES)

    files_in_dir = get_all_regular_files_in_directory(tmp_path)
    filtered_files = list(filter_files(files_in_dir, [lambda _: False]))

    assert len(filtered_files) == 0


def test_filter_files__all_true(tmp_path):
    files = add_files_to_dir(tmp_path, FILES)
    expected_return_value = sorted(files)

    files_in_dir = get_all_regular_files_in_directory(tmp_path)
    filtered_files = filter_files(files_in_dir, [lambda _: True])

    assert sorted(filtered_files) == expected_return_value


def test_filter_files__multiple_filters(tmp_path):
    files = add_files_to_dir(tmp_path, FILES)
    expected_return_value = sorted(files[4:6])

    files_in_dir = get_all_regular_files_in_directory(tmp_path)
    filtered_files = filter_files(
        files_in_dir, [lambda f: f.name.startswith("2"), lambda f: f.name.endswith("g")]
    )

    assert sorted(filtered_files) == expected_return_value


def test_file_extension_filter(tmp_path):
    valid_extensions = {".zip", ".xyz"}

    files = add_files_to_dir(tmp_path, FILES)

    files_in_dir = get_all_regular_files_in_directory(tmp_path)
    filtered_files = filter_files(files_in_dir, [file_extension_filter(valid_extensions)])

    assert sorted(files[0:2]) == sorted(filtered_files)


@pytest.mark.skipif(
    os.name == "nt" and not is_user_admin(), reason="Test requires admin rights on Windows"
)
def test_is_not_symlink_filter(tmp_path):
    files = add_files_to_dir(tmp_path, FILES)
    link_path = tmp_path / "symlink.test"
    link_path.symlink_to(files[0], target_is_directory=False)

    files_in_dir = list(get_all_regular_files_in_directory(tmp_path))
    filtered_files = list(filter_files(files_in_dir, [is_not_symlink_filter]))

    assert link_path in files_in_dir
    assert len(filtered_files) == len(FILES)
    assert link_path not in filtered_files


def test_is_not_shortcut_filter(tmp_path):
    add_files_to_dir(tmp_path, FILES)

    files_in_dir = get_all_regular_files_in_directory(tmp_path)
    filtered_files = list(filter_files(files_in_dir, [is_not_shortcut_filter]))

    assert len(filtered_files) == len(FILES) - 1
    assert SHORTCUT not in [f.name for f in filtered_files]
