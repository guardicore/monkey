import json
import os
import shutil

import pytest

from monkey_island.cc.environment.environment_config import EnvironmentConfig
from monkey_island.cc.environment.user_creds import UserCreds


@pytest.fixture
def config_file(tmpdir):
    return os.path.join(tmpdir, "test_config.json")


def test_get_with_credentials(with_credentials):
    config_dict = EnvironmentConfig(with_credentials).to_dict()

    assert len(config_dict.keys()) == 3
    assert config_dict["server_config"] == "password"
    assert config_dict["user"] == "test"
    assert config_dict["password_hash"] == "abcdef"


def test_get_with_no_credentials(no_credentials):
    config_dict = EnvironmentConfig(no_credentials).to_dict()

    assert len(config_dict.keys()) == 1
    assert config_dict["server_config"] == "password"


def test_get_with_partial_credentials(partial_credentials):
    config_dict = EnvironmentConfig(partial_credentials).to_dict()

    assert len(config_dict.keys()) == 2
    assert config_dict["server_config"] == "password"
    assert config_dict["user"] == "test"


def test_save_to_file(config_file, with_credentials):
    shutil.copyfile(with_credentials, config_file)

    environment_config = EnvironmentConfig(config_file)
    environment_config.aws = "test_aws"
    environment_config.save_to_file()

    with open(config_file, "r") as f:
        from_file = json.load(f)

    assert environment_config.to_dict() == from_file["environment"]


def test_save_to_file_preserve_log_level(config_file, with_credentials):
    shutil.copyfile(with_credentials, config_file)

    environment_config = EnvironmentConfig(config_file)
    environment_config.aws = "test_aws"
    environment_config.save_to_file()

    with open(config_file, "r") as f:
        from_file = json.load(f)

    assert "log_level" in from_file
    assert from_file["log_level"] == "NOTICE"


def test_add_user(config_file, with_credentials):
    new_user = "new_user"
    new_password_hash = "fedcba"
    new_user_creds = UserCreds(new_user, new_password_hash)

    shutil.copyfile(with_credentials, config_file)

    environment_config = EnvironmentConfig(config_file)
    environment_config.add_user(new_user_creds)

    with open(config_file, "r") as f:
        from_file = json.load(f)

    assert len(from_file["environment"].keys()) == 3
    assert from_file["environment"]["user"] == new_user
    assert from_file["environment"]["password_hash"] == new_password_hash


def test_get_user(with_credentials):
    environment_config = EnvironmentConfig(with_credentials)
    user = environment_config.get_user()

    assert user.id == 1
    assert user.username == "test"
    assert user.secret == "abcdef"
