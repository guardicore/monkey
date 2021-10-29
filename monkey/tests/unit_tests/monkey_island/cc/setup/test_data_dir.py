from pathlib import Path

import pytest

from monkey_island.cc.setup.data_dir import IncompatibleDataDirectory, setup_data_dir
from monkey_island.cc.setup.env_utils import DOCKER_ENV_VAR
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
def temp_data_dir_path(tmp_path) -> Path:
    return tmp_path / "data_dir"


@pytest.fixture
def temp_version_file_path(temp_data_dir_path) -> Path:
    return temp_data_dir_path / _version_filename


def create_bogus_file(dir_path: Path) -> Path:
    bogus_file_path = dir_path / "test.txt"
    bogus_file_path.touch()
    return bogus_file_path


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
    bogus_file_path = create_bogus_file(temp_data_dir_path)

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
    bogus_file_path = create_bogus_file(temp_data_dir_path)

    with pytest.raises(IncompatibleDataDirectory):
        setup_data_dir(temp_data_dir_path)

    assert temp_version_file_path.read_text() == old_version
    assert bogus_file_path.is_file()


def test_data_dir_setup_not_needed(temp_data_dir_path, temp_version_file_path):
    temp_data_dir_path.mkdir()
    temp_version_file_path.write_text(current_version)
    bogus_file_path = create_bogus_file(temp_data_dir_path)

    setup_data_dir(temp_data_dir_path)
    assert temp_version_file_path.read_text() == current_version
    assert bogus_file_path.is_file()


def test_empty_data_dir(temp_data_dir_path, temp_version_file_path):
    temp_data_dir_path.mkdir()

    setup_data_dir(temp_data_dir_path)
    assert temp_version_file_path.read_text() == current_version


def test_new_data_dir_docker(monkeypatch, temp_data_dir_path, temp_version_file_path):
    monkeypatch.setenv(DOCKER_ENV_VAR, "true")

    temp_data_dir_path.mkdir()
    bogus_file_path = create_bogus_file(temp_data_dir_path)
    temp_version_file_path.write_text(current_version)

    setup_data_dir(temp_data_dir_path)
    assert temp_version_file_path.read_text() == current_version
    assert bogus_file_path.is_file()


def test_data_dir_docker_old_version(monkeypatch, temp_data_dir_path, temp_version_file_path):
    monkeypatch.setenv(DOCKER_ENV_VAR, "true")

    temp_data_dir_path.mkdir()
    temp_version_file_path.write_text(old_version)

    with pytest.raises(IncompatibleDataDirectory):
        setup_data_dir(temp_data_dir_path)


def test_empty_data_dir_docker(monkeypatch, temp_data_dir_path, temp_version_file_path):
    monkeypatch.setenv(DOCKER_ENV_VAR, "true")

    temp_data_dir_path.mkdir()

    setup_data_dir(temp_data_dir_path)
    assert temp_version_file_path.read_text() == current_version


def test_old_data_dir_docker_no_version(monkeypatch, temp_data_dir_path):
    monkeypatch.setenv(DOCKER_ENV_VAR, "true")

    temp_data_dir_path.mkdir()
    create_bogus_file(temp_data_dir_path)

    with pytest.raises(IncompatibleDataDirectory):
        setup_data_dir(temp_data_dir_path)
