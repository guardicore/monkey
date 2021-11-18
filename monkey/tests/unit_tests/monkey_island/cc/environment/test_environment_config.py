import json
import os
import shutil

import pytest

from monkey_island.cc.environment.environment_config import EnvironmentConfig


@pytest.fixture
def config_file(tmpdir):
    return os.path.join(tmpdir, "test_config.json")


def test_get_with_no_credentials(no_credentials):
    config_dict = EnvironmentConfig(no_credentials).to_dict()

    assert len(config_dict.keys()) == 1
    assert config_dict["server_config"] == "password"


def test_save_to_file(config_file, no_credentials):
    shutil.copyfile(no_credentials, config_file)

    environment_config = EnvironmentConfig(config_file)
    environment_config.aws = "test_aws"
    environment_config.save_to_file()

    with open(config_file, "r") as f:
        from_file = json.load(f)

    assert environment_config.to_dict() == from_file["environment"]
