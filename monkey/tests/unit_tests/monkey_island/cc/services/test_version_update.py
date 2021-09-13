import os

import pytest

from monkey_island.cc.services.version_update import VersionUpdateService


@pytest.fixture
def deployment_file(data_for_tests_dir):
    return os.path.join(data_for_tests_dir, "deployment.json")


def test_get_deployment_field(deployment_file, monkeypatch):
    monkeypatch.setattr(os.path, "join", lambda *args: deployment_file)
    deployment = VersionUpdateService().get_deployment_file()
    assert deployment == "develop"
