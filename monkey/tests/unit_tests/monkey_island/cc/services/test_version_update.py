from pathlib import Path

import pytest

from monkey_island.cc.services.version_update import VersionUpdateService


@pytest.fixture
def deployment_info_file_path(data_for_tests_dir):
    path = data_for_tests_dir / "deployment.json"
    return path


@pytest.fixture
def key_error_deployment_info_file_path(data_for_tests_dir):
    path = data_for_tests_dir / "deployment_key_error.json"
    return path


@pytest.fixture
def flawed_deployment_info_file_path(data_for_tests_dir):
    path = data_for_tests_dir / "deployment_flawed"
    return path


def test_get_deployment_field_from_file(deployment_info_file_path):
    deployment = VersionUpdateService().get_deployment_from_file(deployment_info_file_path)
    assert deployment == "develop"


def test_get_deployment_field_from_nonexistent_file():
    ghost_file = Path("ghost_file")
    deployment = VersionUpdateService().get_deployment_from_file(ghost_file)
    assert deployment == "unknown"


def test_get_deployment_field_key_error(key_error_deployment_info_file_path):
    deployment = VersionUpdateService().get_deployment_from_file(
        key_error_deployment_info_file_path
    )
    assert deployment == "unknown"


def test_get_deployment_field_from_flawed_json_file(flawed_deployment_info_file_path):
    deployment = VersionUpdateService().get_deployment_from_file(flawed_deployment_info_file_path)
    assert deployment == "unknown"
