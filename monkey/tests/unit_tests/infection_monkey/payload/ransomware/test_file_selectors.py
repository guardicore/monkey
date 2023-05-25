import os
import shutil
from pathlib import Path

import pytest
from tests.unit_tests.infection_monkey.payload.ransomware.ransomware_target_files import (
    ALL_ZEROS_PDF,
    HELLO_TXT,
    GOODBYE_TXT,
    FOO_JPG,
    SHORTCUT_LNK,
    SUBDIR1,
    SUBDIR1A,
    SUBDIR2,
    TEST_KEYBOARD_TXT,
    TEST_LIB_DLL,
)
from tests.utils import is_user_admin

from infection_monkey.payload.ransomware.file_selectors import ProductionSafeTargetFileSelector
from infection_monkey.payload.ransomware.ransomware import README_SRC

TARGETED_FILE_EXTENSIONS = {".pdf", ".txt", ".jpg"}


@pytest.fixture
def file_selector():
    return ProductionSafeTargetFileSelector(TARGETED_FILE_EXTENSIONS)


def test_select_targeted_files_only(ransomware_test_data, file_selector):
    selected_files = list(file_selector(ransomware_test_data))

    assert len(selected_files) == 2
    assert (ransomware_test_data / ALL_ZEROS_PDF) in selected_files
    assert (ransomware_test_data / TEST_KEYBOARD_TXT) in selected_files


def test_shortcut_not_selected(ransomware_test_data):
    extensions = TARGETED_FILE_EXTENSIONS.union({".lnk"})
    file_selector = ProductionSafeTargetFileSelector(extensions)

    selected_files = file_selector(ransomware_test_data)
    assert ransomware_test_data / SHORTCUT_LNK not in selected_files


@pytest.mark.skipif(
    os.name == "nt" and not is_user_admin(), reason="Test requires admin rights on Windows"
)
def test_symlink_not_selected(ransomware_target, file_selector):
    SYMLINK = "symlink.pdf"
    link_path = ransomware_target / SYMLINK
    link_path.symlink_to(ransomware_target / TEST_LIB_DLL)

    selected_files = file_selector(ransomware_target)
    assert link_path not in selected_files


def test_directories_not_selected(ransomware_test_data, file_selector):
    selected_files = file_selector(ransomware_test_data)

    assert (ransomware_test_data / SUBDIR1 / HELLO_TXT) not in selected_files
    assert (ransomware_test_data / SUBDIR1 / SUBDIR1A / GOODBYE_TXT) not in selected_files
    assert (ransomware_test_data / SUBDIR2 / FOO_JPG) not in selected_files


def test_ransomware_readme_not_selected(ransomware_target, file_selector):
    readme_file = ransomware_target / "README.txt"
    shutil.copyfile(README_SRC, readme_file)

    selected_files = file_selector(ransomware_target)

    assert readme_file not in selected_files


def test_pre_existing_readme_is_selected(ransomware_target, stable_file, file_selector):
    readme_file = ransomware_target / "README.txt"
    shutil.copyfile(stable_file, readme_file)

    selected_files = file_selector(ransomware_target)

    assert readme_file in selected_files


def test_directory_doesnt_exist(file_selector):
    selected_files = file_selector(Path("/nonexistent"))

    assert len(list(selected_files)) == 0


def test_target_directory_is_file(tmp_path, file_selector):
    target_file = tmp_path / "target_file.txt"
    target_file.touch()
    assert target_file.exists()
    assert target_file.is_file()

    selected_files = file_selector(target_file)

    assert len(list(selected_files)) == 0


@pytest.mark.skipif(
    os.name == "nt" and not is_user_admin(), reason="Test requires admin rights on Windows"
)
def test_target_directory_is_symlink(tmp_path, ransomware_test_data, file_selector):
    link_directory = tmp_path / "link_directory"
    link_directory.symlink_to(ransomware_test_data, target_is_directory=True)
    assert len(list(link_directory.iterdir())) > 0

    selected_files = file_selector(link_directory)

    assert len(list(selected_files)) == 0
