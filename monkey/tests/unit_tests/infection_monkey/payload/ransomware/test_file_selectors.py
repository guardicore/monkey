import os
import shutil
from pathlib import Path

import pytest
from tests.unit_tests.infection_monkey.payload.ransomware.ransomware_target_files import (
    ALL_ZEROS_PDF,
    FOO_JPG,
    GOODBYE_TXT,
    HELLO_TXT,
    SHORTCUT_LNK,
    SUBDIR1,
    SUBDIR1A,
    SUBDIR2,
    TEST_KEYBOARD_TXT,
    TEST_LIB_DLL,
)
from tests.utils import is_user_admin

from infection_monkey.payload.ransomware.file_selectors import (
    ProductionSafeTargetFileSelector,
    RecursiveTargetFileSelector,
)
from infection_monkey.payload.ransomware.ransomware import README_SRC

TARGETED_FILE_EXTENSIONS = {".pdf", ".txt", ".jpg"}


@pytest.fixture
def production_safe_file_selector():
    return ProductionSafeTargetFileSelector(TARGETED_FILE_EXTENSIONS)


@pytest.fixture
def recursive_file_selector():
    return RecursiveTargetFileSelector(TARGETED_FILE_EXTENSIONS)


def test_select_targeted_files_only__production_safe(
    ransomware_test_data, production_safe_file_selector
):
    selected_files = list(production_safe_file_selector(ransomware_test_data))

    assert len(selected_files) == 2
    assert (ransomware_test_data / ALL_ZEROS_PDF) in selected_files
    assert (ransomware_test_data / TEST_KEYBOARD_TXT) in selected_files


def test_select_targeted_files_only__recursive(ransomware_test_data, recursive_file_selector):
    selected_files = list(recursive_file_selector(ransomware_test_data))

    assert (ransomware_test_data / ALL_ZEROS_PDF) in selected_files
    assert (ransomware_test_data / TEST_KEYBOARD_TXT) in selected_files
    assert (ransomware_test_data / SUBDIR1 / HELLO_TXT) in selected_files
    assert (ransomware_test_data / SUBDIR2 / FOO_JPG) in selected_files
    assert (ransomware_test_data / SUBDIR1 / SUBDIR1A / GOODBYE_TXT) in selected_files
    assert len(selected_files) == 5


def test_shortcut_not_selected__production_safe(ransomware_test_data):
    extensions = TARGETED_FILE_EXTENSIONS.union({".lnk"})
    production_safe_file_selector = ProductionSafeTargetFileSelector(extensions)

    selected_files = production_safe_file_selector(ransomware_test_data)
    assert ransomware_test_data / SHORTCUT_LNK not in selected_files


def test_shortcut_not_selected__recursive(ransomware_test_data):
    extensions = TARGETED_FILE_EXTENSIONS.union({".lnk"})
    production_safe_file_selector = RecursiveTargetFileSelector(extensions)

    selected_files = production_safe_file_selector(ransomware_test_data)
    assert ransomware_test_data / SHORTCUT_LNK not in selected_files


@pytest.mark.skipif(
    os.name == "nt" and not is_user_admin(), reason="Test requires admin rights on Windows"
)
@pytest.mark.parametrize(
    "file_selector", ["production_safe_file_selector", "recursive_file_selector"]
)
def test_symlink_not_selected(ransomware_target, file_selector, request):
    SYMLINK = "symlink.pdf"
    link_path = ransomware_target / SYMLINK
    link_path.symlink_to(ransomware_target / TEST_LIB_DLL)

    selected_files = request.getfixturevalue(file_selector)(ransomware_target)
    assert link_path not in selected_files


def test_directories_not_selected(ransomware_test_data, production_safe_file_selector):
    selected_files = production_safe_file_selector(ransomware_test_data)

    assert (ransomware_test_data / SUBDIR1 / HELLO_TXT) not in selected_files
    assert (ransomware_test_data / SUBDIR1 / SUBDIR1A / GOODBYE_TXT) not in selected_files
    assert (ransomware_test_data / SUBDIR2 / FOO_JPG) not in selected_files


@pytest.mark.parametrize(
    "file_selector", ["production_safe_file_selector", "recursive_file_selector"]
)
def test_ransomware_readme_not_selected(ransomware_target, file_selector, request):
    readme_file = ransomware_target / "README.txt"
    shutil.copyfile(README_SRC, readme_file)

    selected_files = request.getfixturevalue(file_selector)(ransomware_target)

    assert readme_file not in selected_files


@pytest.mark.parametrize(
    "file_selector", ["production_safe_file_selector", "recursive_file_selector"]
)
def test_pre_existing_readme_is_selected(ransomware_target, stable_file, file_selector, request):
    readme_file = ransomware_target / "README.txt"
    shutil.copyfile(stable_file, readme_file)

    selected_files = request.getfixturevalue(file_selector)(ransomware_target)

    assert readme_file in selected_files


@pytest.mark.parametrize(
    "file_selector", ["production_safe_file_selector", "recursive_file_selector"]
)
def test_directory_doesnt_exist(file_selector, request):
    selected_files = request.getfixturevalue(file_selector)(Path("/nonexistent"))

    assert len(list(selected_files)) == 0


@pytest.mark.parametrize(
    "file_selector", ["production_safe_file_selector", "recursive_file_selector"]
)
def test_target_directory_is_file(tmp_path, file_selector, request):
    target_file = tmp_path / "target_file.txt"
    target_file.touch()
    assert target_file.exists()
    assert target_file.is_file()

    selected_files = request.getfixturevalue(file_selector)(target_file)

    assert len(list(selected_files)) == 0


@pytest.mark.skipif(
    os.name == "nt" and not is_user_admin(), reason="Test requires admin rights on Windows"
)
@pytest.mark.parametrize(
    "file_selector", ["production_safe_file_selector", "recursive_file_selector"]
)
def test_target_directory_is_symlink(tmp_path, ransomware_test_data, file_selector, request):
    link_directory = tmp_path / "link_directory"
    link_directory.symlink_to(ransomware_test_data, target_is_directory=True)
    assert len(list(link_directory.iterdir())) > 0

    selected_files = request.getfixturevalue(file_selector)(link_directory)

    assert len(list(selected_files)) == 0
