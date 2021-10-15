from pathlib import Path

import pytest

from monkey_island.cc.setup.data_dir import setup_data_dir
from monkey_island.cc.setup.version_file_setup import _version_filename

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

    # mock version
    setup_data_dir(mocked_data_dir_path)

    assert mocked_version_file_path.read_text() == current_version
    assert not bogus_file_path.is_file()


def test_data_dir_setup_not_needed(mocked_data_dir_path, mocked_version_file_path):
    mocked_data_dir_path.mkdir()
    mocked_version_file_path.write_text(current_version)
    bogus_file_path = mocked_data_dir_path.joinpath("test.txt")
    bogus_file_path.touch()

    setup_data_dir(mocked_data_dir_path)
    assert mocked_version_file_path.read_text() == current_version
    assert bogus_file_path.is_file()
