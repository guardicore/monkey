from pathlib import Path

import pytest


@pytest.fixture
def plugin_file(plugin_data_dir) -> Path:
    return plugin_data_dir / "test-exploiter.tar"


@pytest.fixture
def missing_manifest_plugin_file(plugin_data_dir) -> Path:
    return plugin_data_dir / "missing-manifest.tar"


@pytest.fixture
def bad_plugin_file(plugin_data_dir) -> Path:
    return plugin_data_dir / "bad-exploiter.tar"


@pytest.fixture
def symlink_plugin_file(plugin_data_dir) -> Path:
    return plugin_data_dir / "symlink-exploiter.tar"


@pytest.fixture
def dir_plugin_file(plugin_data_dir) -> Path:
    return plugin_data_dir / "dir-exploiter.tar"
