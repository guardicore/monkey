from json import dumps
from pathlib import Path

import pytest

import monkey_island.cc.setup.config_setup  # noqa: F401
from monkey_island.cc.arg_parser import IslandCmdArgs
from monkey_island.cc.server_setup import _extract_config
from monkey_island.cc.setup.island_config_options import IslandConfigOptions

BAD_JSON = '{"data_dir": "C:\\test\\test"'


@pytest.fixture
def user_server_config_path(tmpdir) -> Path:
    return tmpdir / "fake_server_config.json"


@pytest.fixture
def deployment_server_config_path(tmpdir) -> Path:
    return tmpdir / "fake_server_config2.json"


def create_server_config(config_contents: str, server_config_path: Path):
    with open(server_config_path, "w") as file:
        file.write(config_contents)


@pytest.fixture(autouse=True)
def mock_deployment_config_path(monkeypatch, deployment_server_config_path):
    monkeypatch.setattr(
        "monkey_island.cc.setup.config_setup.DEFAULT_SERVER_CONFIG_PATH",
        deployment_server_config_path,
    )


def test_extract_config_defaults():
    expected = IslandConfigOptions({})
    assert (
        expected.__dict__
        == _extract_config(IslandCmdArgs(setup_only=False, server_config_path=None)).__dict__
    )


def test_package_config_overrides_defaults(deployment_server_config_path):
    expected = IslandConfigOptions({"key_path": "/key_path_2"})
    create_server_config(dumps({"key_path": "/key_path_2"}), deployment_server_config_path)
    assert (
        expected.__dict__
        == _extract_config(IslandCmdArgs(setup_only=False, server_config_path=None)).__dict__
    )


def test_user_config_overrides_package_config(
    deployment_server_config_path, user_server_config_path
):
    expected = IslandConfigOptions({"key_path": "/key_path_3"})
    create_server_config(dumps({"key_path": "/key_path_2"}), deployment_server_config_path)
    create_server_config(dumps({"key_path": "/key_path_3"}), user_server_config_path)
    extracted_config = _extract_config(
        IslandCmdArgs(setup_only=False, server_config_path=user_server_config_path)
    )
    assert expected.__dict__ == extracted_config.__dict__


def test_malformed_json(user_server_config_path):
    create_server_config(BAD_JSON, user_server_config_path)
    with pytest.raises(SystemExit):
        _extract_config(IslandCmdArgs(setup_only=False, server_config_path=user_server_config_path))
