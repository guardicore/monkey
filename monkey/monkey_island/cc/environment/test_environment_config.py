import json
import os
from typing import Dict

import pytest

import monkey_island.cc.testing.environment.server_config_mocks as config_mocks
from monkey_island.cc.environment.environment_config import EnvironmentConfig
from monkey_island.cc.environment.user_creds import UserCreds


@pytest.fixture
def config_file(tmpdir):
    return os.path.join(tmpdir, "test_config.json")


def test_get_with_credentials(config_file):
    test_conf = config_mocks.CONFIG_WITH_CREDENTIALS

    _write_test_config_to_tmp(config_file, test_conf)
    config_dict = EnvironmentConfig.get_from_file(config_file).to_dict()

    assert len(config_dict.keys()) == 4
    assert config_dict["server_config"] == test_conf["server_config"]
    assert config_dict["deployment"] == test_conf["deployment"]
    assert config_dict["user"] == test_conf["user"]
    assert config_dict["password_hash"] == test_conf["password_hash"]


def test_get_with_no_credentials(config_file):
    test_conf = config_mocks.CONFIG_NO_CREDENTIALS

    _write_test_config_to_tmp(config_file, test_conf)
    config_dict = EnvironmentConfig.get_from_file(config_file).to_dict()

    assert len(config_dict.keys()) == 2
    assert config_dict["server_config"] == test_conf["server_config"]
    assert config_dict["deployment"] == test_conf["deployment"]


def test_get_with_partial_credentials(config_file):
    test_conf = config_mocks.CONFIG_PARTIAL_CREDENTIALS

    _write_test_config_to_tmp(config_file, test_conf)
    config_dict = EnvironmentConfig.get_from_file(config_file).to_dict()

    assert len(config_dict.keys()) == 3
    assert config_dict["server_config"] == test_conf["server_config"]
    assert config_dict["deployment"] == test_conf["deployment"]
    assert config_dict["user"] == test_conf["user"]


def _write_test_config_to_tmp(config_file, config: Dict):
    with open(config_file, "wt") as f:
        json.dump(config, f)


def test_save_to_file(config_file):
    server_config = "standard"
    deployment = "develop"
    user = "test_user"
    password_hash = "abcdef"
    aws = "test"

    environment_config = EnvironmentConfig(
        server_config, deployment, UserCreds(user, password_hash), aws
    )
    environment_config.server_config_path = config_file

    environment_config.save_to_file()
    with open(config_file, "r") as f:
        from_file = json.load(f)

    assert len(from_file.keys()) == 5
    assert from_file["server_config"] == server_config
    assert from_file["deployment"] == deployment
    assert from_file["user"] == user
    assert from_file["password_hash"] == password_hash
    assert from_file["aws"] == aws


def test_add_user(config_file):
    server_config = "standard"
    deployment = "develop"
    user = "test_user"
    password_hash = "abcdef"

    new_user = "new_user"
    new_password_hash = "fedcba"
    new_user_creds = UserCreds(new_user, new_password_hash)

    environment_config = EnvironmentConfig(
        server_config, deployment, UserCreds(user, password_hash)
    )
    environment_config.server_config_path = config_file

    environment_config.add_user(new_user_creds)

    with open(config_file, "r") as f:
        from_file = json.load(f)

    assert len(from_file.keys()) == 4
    assert from_file["user"] == new_user
    assert from_file["password_hash"] == new_password_hash


def test_get_users():
    server_config = "standard"
    deployment = "develop"
    user = "test_user"
    password_hash = "abcdef"

    environment_config = EnvironmentConfig(
        server_config, deployment, UserCreds(user, password_hash)
    )

    users = environment_config.get_users()
    assert len(users) == 1
    assert users[0].id == 1
    assert users[0].username == user
    assert users[0].secret == password_hash
