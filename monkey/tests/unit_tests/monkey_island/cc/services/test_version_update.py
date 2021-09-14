import os

import pytest

from monkey_island.cc.services.version_update import VersionUpdateService


@pytest.fixture
def deployment_info_file_path(data_for_tests_dir):
    return os.path.join(data_for_tests_dir, "deployment.json")


@pytest.fixture
def ghost_file():
    return "ghost_file"


@pytest.fixture
def key_error_deployment_info_file_path(data_for_tests_dir):
    return os.path.join(data_for_tests_dir, "deployment_key_error.json")


@pytest.fixture
def flawed_deployment_info_file_path(data_for_tests_dir):
    return os.path.join(data_for_tests_dir, "deployment_flawed")


def test_get_deployment_field_from_file(deployment_info_file_path, monkeypatch):
    monkeypatch.setattr(os.path, "join", lambda *args: deployment_info_file_path)
    deployment = VersionUpdateService().get_deployment_from_file(deployment_info_file_path)
    assert deployment == "develop"


def test_get_deployment_field_from_nonexistent_file(ghost_file, monkeypatch):
    monkeypatch.setattr(os.path, "join", lambda *args: ghost_file)
    deployment = VersionUpdateService().get_deployment_from_file(ghost_file)
    assert deployment == "unknown"


def test_get_deployment_field_key_error(key_error_deployment_info_file_path, monkeypatch):
    monkeypatch.setattr(os.path, "join", lambda *args: key_error_deployment_info_file_path)
    deployment = VersionUpdateService().get_deployment_from_file(
        key_error_deployment_info_file_path
    )
    assert deployment == "unknown"


def test_get_deployment_field_from_flawed_json_file(flawed_deployment_info_file_path, monkeypatch):
    monkeypatch.setattr(os.path, "join", lambda *args: flawed_deployment_info_file_path)
    deployment = VersionUpdateService().get_deployment_from_file(flawed_deployment_info_file_path)
    assert deployment == "unknown"
