from pathlib import Path
from unittest.mock import Mock

import pytest

from monkey_island.cc.arg_parser import IslandCmdArgs
from monkey_island.cc.setup import create_data_dir


@pytest.fixture
def mock_server_config(monkeypatch, tmpdir):
    mock_config = Mock()
    mock_config.data_dir = Path(tmpdir, "test_data_dir")

    monkeypatch.setattr(
        "monkey_island.cc.setup.data_dir.server_config_handler.load_server_config_from_file",
        lambda _: mock_config,
    )
    return mock_config


def test_create_data_dir__from_args(mock_server_config):
    island_args = IslandCmdArgs(setup_only=False, server_config_path=mock_server_config.data_dir)
    assert create_data_dir(island_args) == str(mock_server_config.data_dir)
    assert mock_server_config.data_dir.is_dir()


def test_create_data_dir__from_defaults(mock_server_config):
    island_args = IslandCmdArgs(setup_only=False, server_config_path="")
    assert create_data_dir(island_args) == str(mock_server_config.data_dir)
    assert mock_server_config.data_dir.is_dir()
