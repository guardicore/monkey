from pathlib import Path

import pytest

from monkey_island.cc.setup.data_dir import IncompatibleDataDirectory, setup_data_dir
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
def temp_data_dir_path(tmpdir) -> Path:
    return Path(tmpdir, "data_dir")


@pytest.fixture
def temp_version_file_path(temp_data_dir_path) -> Path:
    return temp_data_dir_path.joinpath(_version_filename)


def test_setup_data_dir(temp_data_dir_path, temp_version_file_path):
    data_dir_path = temp_data_dir_path
    setup_data_dir(data_dir_path)
    assert data_dir_path.is_dir()

    version_file_path = temp_version_file_path
    assert version_file_path.read_text() == current_version


def test_old_version_removed(monkeypatch, temp_data_dir_path, temp_version_file_path):
    monkeypatch.setattr("builtins.input", lambda _: "y")

    temp_data_dir_path.mkdir()
    temp_version_file_path.write_text(old_version)
    bogus_file_path = temp_data_dir_path.joinpath("test.txt")
    bogus_file_path.touch()

    setup_data_dir(temp_data_dir_path)

    assert temp_version_file_path.read_text() == current_version
    assert not bogus_file_path.is_file()


@pytest.mark.parametrize("input_value", ["n", "x"])
def test_old_version_not_removed(
    monkeypatch, temp_data_dir_path, temp_version_file_path, input_value
):
    monkeypatch.setattr("builtins.input", lambda _: input_value)

    temp_data_dir_path.mkdir()
    temp_version_file_path.write_text(old_version)
    bogus_file_path = temp_data_dir_path.joinpath("test.txt")
    bogus_file_path.touch()

    with pytest.raises(IncompatibleDataDirectory):
        setup_data_dir(temp_data_dir_path)

    assert temp_version_file_path.read_text() == old_version
    assert bogus_file_path.is_file()


def test_data_dir_setup_not_needed(temp_data_dir_path, temp_version_file_path):
    temp_data_dir_path.mkdir()
    temp_version_file_path.write_text(current_version)
    bogus_file_path = temp_data_dir_path.joinpath("test.txt")
    bogus_file_path.touch()

    setup_data_dir(temp_data_dir_path)
    assert temp_version_file_path.read_text() == current_version
    assert bogus_file_path.is_file()
