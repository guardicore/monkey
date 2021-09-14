import os

import pytest

from monkey_island.cc.services.version_update import VersionUpdateService


@pytest.fixture
def deployment_info_file_path(data_for_tests_dir):
    return os.path.join(data_for_tests_dir, "deployment.json")


def test_get_deployment_field(deployment_info_file_path, monkeypatch):
    monkeypatch.setattr(os.path, "join", lambda *args: deployment_info_file_path)
    deployment = VersionUpdateService().get_deployment_from_file(deployment_info_file_path)
    assert deployment == "develop"
