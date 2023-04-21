from pathlib import Path

import pytest
from tests.monkey_island.utils import assert_linux_permissions, assert_windows_permissions

from common.utils.environment import is_windows_os
from monkey_island.cc.server_utils.consts import PLUGIN_DIR_NAME
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


def test_plugin_dir_created(temp_data_dir_path):
    setup_data_dir(temp_data_dir_path)
    assert (temp_data_dir_path / PLUGIN_DIR_NAME).is_dir()


def test_plugin_dir_permissions(temp_data_dir_path):
    setup_data_dir(temp_data_dir_path)
    if is_windows_os():
        assert_windows_permissions(temp_data_dir_path / PLUGIN_DIR_NAME)
    else:
        assert_linux_permissions(temp_data_dir_path / PLUGIN_DIR_NAME)


def test_plugins_copied_to_plugin_dir(monkeypatch, tmp_path, temp_data_dir_path):
    plugin_contents = "test plugin"
    plugin_src_dir = tmp_path / PLUGIN_DIR_NAME
    plugin_src_dir.mkdir()
    test_plugin = plugin_src_dir / "test_plugin.tar"
    test_plugin.write_text(plugin_contents)
    monkeypatch.setattr("monkey_island.cc.setup.data_dir.MONKEY_ISLAND_ABS_PATH", tmp_path)

    setup_data_dir(temp_data_dir_path)
    assert (temp_data_dir_path / PLUGIN_DIR_NAME / test_plugin.name).read_text() == plugin_contents


def test_plugins_in_plugin_dir_not_overwitten(
    monkeypatch, tmp_path, temp_data_dir_path, temp_version_file_path
):
    temp_data_dir_path.mkdir()
    temp_version_file_path.write_text(current_version)

    test_plugin_name = "test_plugin.tar"
    original_plugin_contents = "original plugin"
    plugin_dir = temp_data_dir_path / PLUGIN_DIR_NAME
    plugin_dir.mkdir()
    plugin_dir_plugin = plugin_dir / test_plugin_name
    plugin_dir_plugin.write_text(original_plugin_contents)

    plugin_src_dir = tmp_path / PLUGIN_DIR_NAME
    plugin_src_dir.mkdir()
    new_plugin = plugin_src_dir / test_plugin_name
    new_plugin.write_text("new plugin")
    monkeypatch.setattr("monkey_island.cc.setup.data_dir.MONKEY_ISLAND_ABS_PATH", tmp_path)

    setup_data_dir(temp_data_dir_path)

    assert plugin_dir_plugin.read_text() == original_plugin_contents
