from pathlib import Path

import pytest


@pytest.fixture
def plugin_file(plugin_data_dir) -> Path:
    return plugin_data_dir / "test-exploiter.tar"


@pytest.fixture
def plugin_with_one_vendor_file(plugin_data_dir) -> Path:
    return plugin_data_dir / "plugin-with-one-vendor.tar"


@pytest.fixture
def plugin_with_two_vendors_file(plugin_data_dir) -> Path:
    return plugin_data_dir / "plugin-with-two-vendors.tar"


@pytest.fixture
def bad_plugin_file(plugin_data_dir) -> Path:
    return plugin_data_dir / "bad-exploiter.tar"


@pytest.fixture
def symlink_plugin_file(plugin_data_dir) -> Path:
    return plugin_data_dir / "symlink-exploiter.tar"


@pytest.fixture
def dir_plugin_file(plugin_data_dir) -> Path:
    return plugin_data_dir / "dir-exploiter.tar"


@pytest.fixture
def plugin_with_three_vendors_file(plugin_data_dir) -> Path:
    return plugin_data_dir / "plugin-with-three-vendors.tar"


@pytest.fixture
def plugin_with_two_vendor_dirs_one_vendor_file_file(plugin_data_dir) -> Path:
    return plugin_data_dir / "plugin-with-two-vendor-dir-one-vendor-file.tar"


@pytest.fixture
def only_windows_vendor_plugin_file(plugin_data_dir) -> Path:
    return plugin_data_dir / "only-windows-vendor-plugin-file.tar"
