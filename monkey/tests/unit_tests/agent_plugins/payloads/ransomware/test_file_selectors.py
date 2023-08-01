import os
import shutil
from pathlib import Path

import pytest
from agent_plugins.payloads.ransomware.src.file_selectors import (
    README_SRC,
    ProductionSafeTargetFileSelector,
)
from agent_plugins.payloads.ransomware.src.typedef import FileSelectorCallable
from tests.unit_tests.agent_plugins.payloads.ransomware.ransomware_target_files import (
    ALL_ZEROS_PDF,
    HELLO_TXT,
    SHORTCUT_LNK,
    SUBDIR,
    TEST_KEYBOARD_TXT,
    TEST_LIB_DLL,
)
from tests.utils import is_user_admin

TARGETED_FILE_EXTENSIONS = [".pdf", ".txt"]


@pytest.fixture
def file_selector() -> FileSelectorCallable:
    return ProductionSafeTargetFileSelector(set(TARGETED_FILE_EXTENSIONS))


def test_select_targeted_files_only(
    ransomware_test_data: Path, file_selector: FileSelectorCallable
):
    selected_files = list(file_selector(ransomware_test_data))

    assert len(selected_files) == 2
    assert (ransomware_test_data / ALL_ZEROS_PDF) in selected_files
    assert (ransomware_test_data / TEST_KEYBOARD_TXT) in selected_files


def test_shortcut_not_selected(ransomware_test_data: Path):
    extensions = set(TARGETED_FILE_EXTENSIONS + [".lnk"])
    file_selector = ProductionSafeTargetFileSelector(extensions)

    selected_files = file_selector(ransomware_test_data)
    assert ransomware_test_data / SHORTCUT_LNK not in selected_files


@pytest.mark.skipif(
    os.name == "nt" and not is_user_admin(), reason="Test requires admin rights on Windows"
)
def test_symlink_not_selected(ransomware_target: Path, file_selector: FileSelectorCallable):
    SYMLINK = "symlink.pdf"
    link_path = ransomware_target / SYMLINK
    link_path.symlink_to(ransomware_target / TEST_LIB_DLL)

    selected_files = file_selector(ransomware_target)
    assert link_path not in selected_files


def test_directories_not_selected(ransomware_test_data: Path, file_selector: FileSelectorCallable):
    selected_files = file_selector(ransomware_test_data)

    assert (ransomware_test_data / SUBDIR / HELLO_TXT) not in selected_files


def test_ransomware_readme_not_selected(
    ransomware_target: Path, file_selector: FileSelectorCallable
):
    readme_file = ransomware_target / "README.txt"
    shutil.copyfile(README_SRC, readme_file)

    selected_files = file_selector(ransomware_target)

    assert readme_file not in selected_files


def test_pre_existing_readme_is_selected(
    ransomware_target: Path, stable_file: Path, file_selector: FileSelectorCallable
):
    readme_file = ransomware_target / "README.txt"
    shutil.copyfile(stable_file, readme_file)

    selected_files = file_selector(ransomware_target)

    assert readme_file in selected_files


def test_directory_doesnt_exist(file_selector: FileSelectorCallable):
    selected_files = file_selector(Path("/nonexistent"))

    assert len(list(selected_files)) == 0


def test_target_directory_is_file(tmp_path: Path, file_selector: FileSelectorCallable):
    target_file = tmp_path / "target_file.txt"
    target_file.touch()
    assert target_file.exists()
    assert target_file.is_file()

    selected_files = file_selector(target_file)

    assert len(list(selected_files)) == 0


@pytest.mark.skipif(
    os.name == "nt" and not is_user_admin(), reason="Test requires admin rights on Windows"
)
def test_target_directory_is_symlink(
    tmp_path: Path, ransomware_test_data: Path, file_selector: FileSelectorCallable
):
    link_directory = tmp_path / "link_directory"
    link_directory.symlink_to(ransomware_test_data, target_is_directory=True)
    assert len(list(link_directory.iterdir())) > 0

    selected_files = file_selector(link_directory)

    assert len(list(selected_files)) == 0
