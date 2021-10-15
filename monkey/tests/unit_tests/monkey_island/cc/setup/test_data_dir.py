from pathlib import Path

import pytest

from monkey_island.cc.setup.data_dir import _get_backup_path, setup_data_dir
from monkey_island.cc.setup.version_file_setup import _version_filename, get_version_from_dir

current_version = "1.1.1"
old_version = "1.1.0"


@pytest.fixture(autouse=True)
def mock_version(monkeypatch):
    monkeypatch.setattr("monkey_island.cc.setup.data_dir.get_version", lambda: current_version)
    monkeypatch.setattr(
        "monkey_island.cc.setup.version_file_setup.get_version", lambda: current_version
    )


@pytest.fixture
def mocked_data_dir_path(tmpdir) -> Path:
    return Path(tmpdir, "data_dir")


@pytest.fixture
def mocked_version_file_path(mocked_data_dir_path: Path) -> Path:
    return mocked_data_dir_path.joinpath(_version_filename)


def test_setup_data_dir(mocked_data_dir_path, mocked_version_file_path):
    data_dir_path = mocked_data_dir_path
    setup_data_dir(data_dir_path)
    assert data_dir_path.is_dir()

    version_file_path = mocked_version_file_path
    assert version_file_path.read_text() == current_version


def test_old_version_present(mocked_data_dir_path, mocked_version_file_path):
    mocked_data_dir_path.mkdir()
    mocked_version_file_path.write_text(old_version)
    bogus_file_path = mocked_data_dir_path.joinpath("test.txt")
    bogus_file_path.touch()

    setup_data_dir(mocked_data_dir_path)

    assert mocked_version_file_path.read_text() == current_version
    assert not bogus_file_path.is_file()
    assert _get_backup_path(mocked_data_dir_path).joinpath("test.txt").is_file()


def test_old_version_and_backup_present(mocked_data_dir_path, mocked_version_file_path):
    mocked_data_dir_path.mkdir()
    mocked_version_file_path.write_text(old_version)

    old_backup_path = _get_backup_path(mocked_data_dir_path)
    old_backup_path.mkdir()
    bogus_file_path = old_backup_path.joinpath("test.txt")
    bogus_file_path.touch()

    setup_data_dir(mocked_data_dir_path)
    new_backup_path = old_backup_path

    # Make sure old backup got deleted and new backup took it's place
    assert mocked_version_file_path.read_text() == current_version
    assert get_version_from_dir(new_backup_path) == old_version
    assert not _get_backup_path(mocked_data_dir_path).joinpath("test.txt").is_file()


def test_data_dir_setup_not_needed(mocked_data_dir_path, mocked_version_file_path):
    mocked_data_dir_path.mkdir()
    mocked_version_file_path.write_text(current_version)
    bogus_file_path = mocked_data_dir_path.joinpath("test.txt")
    bogus_file_path.touch()

    setup_data_dir(mocked_data_dir_path)
    assert mocked_version_file_path.read_text() == current_version
    assert bogus_file_path.is_file()
