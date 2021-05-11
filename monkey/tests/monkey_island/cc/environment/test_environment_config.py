import json
import os
import shutil

import pytest

from monkey_island.cc.environment.environment_config import EnvironmentConfig
from monkey_island.cc.environment.user_creds import UserCreds
from monkey_island.cc.server_utils.consts import DEFAULT_DATA_DIR


@pytest.fixture
def config_file(tmpdir):
    return os.path.join(tmpdir, "test_config.json")


def test_get_with_credentials(with_credentials):
    config_dict = EnvironmentConfig(with_credentials).to_dict()

    assert len(config_dict.keys()) == 5
    assert config_dict["server_config"] == "password"
    assert config_dict["deployment"] == "develop"
    assert config_dict["user"] == "test"
    assert config_dict["password_hash"] == "abcdef"
    assert config_dict["data_dir"] == DEFAULT_DATA_DIR


def test_get_with_no_credentials(no_credentials):
    config_dict = EnvironmentConfig(no_credentials).to_dict()

    assert len(config_dict.keys()) == 3
    assert config_dict["server_config"] == "password"
    assert config_dict["deployment"] == "develop"
    assert config_dict["data_dir"] == DEFAULT_DATA_DIR


def test_get_with_partial_credentials(partial_credentials):
    config_dict = EnvironmentConfig(partial_credentials).to_dict()

    assert len(config_dict.keys()) == 4
    assert config_dict["server_config"] == "password"
    assert config_dict["deployment"] == "develop"
    assert config_dict["user"] == "test"
    assert config_dict["data_dir"] == DEFAULT_DATA_DIR


def test_save_to_file(config_file, standard_with_credentials):
    shutil.copyfile(standard_with_credentials, config_file)

    environment_config = EnvironmentConfig(config_file)
    environment_config.aws = "test_aws"
    environment_config.save_to_file()

    with open(config_file, "r") as f:
        from_file = json.load(f)

    assert len(from_file.keys()) == 2
    assert len(from_file["environment"].keys()) == 6
    assert from_file["environment"]["server_config"] == "standard"
    assert from_file["environment"]["deployment"] == "develop"
    assert from_file["environment"]["user"] == "test"
    assert from_file["environment"]["password_hash"] == "abcdef"
    assert from_file["environment"]["aws"] == "test_aws"
    assert from_file["environment"]["data_dir"] == DEFAULT_DATA_DIR


def test_save_to_file_preserve_log_level(config_file, standard_with_credentials):
    shutil.copyfile(standard_with_credentials, config_file)

    environment_config = EnvironmentConfig(config_file)
    environment_config.aws = "test_aws"
    environment_config.save_to_file()

    with open(config_file, "r") as f:
        from_file = json.load(f)

    assert len(from_file.keys()) == 2
    assert "log_level" in from_file
    assert from_file["log_level"] == "NOTICE"


def test_add_user(config_file, standard_with_credentials):
    new_user = "new_user"
    new_password_hash = "fedcba"
    new_user_creds = UserCreds(new_user, new_password_hash)

    shutil.copyfile(standard_with_credentials, config_file)

    environment_config = EnvironmentConfig(config_file)
    environment_config.add_user(new_user_creds)

    with open(config_file, "r") as f:
        from_file = json.load(f)

    assert len(from_file["environment"].keys()) == 5
    assert from_file["environment"]["user"] == new_user
    assert from_file["environment"]["password_hash"] == new_password_hash


def test_get_users(standard_with_credentials):
    environment_config = EnvironmentConfig(standard_with_credentials)
    users = environment_config.get_users()

    assert len(users) == 1
    assert users[0].id == 1
    assert users[0].username == "test"
    assert users[0].secret == "abcdef"


def test_generate_default_file(config_file):
    environment_config = EnvironmentConfig(config_file)

    assert os.path.isfile(config_file)

    assert environment_config.server_config == "password"
    assert environment_config.deployment == "develop"
    assert environment_config.user_creds.username == ""
    assert environment_config.user_creds.password_hash == ""
    assert environment_config.aws is None
    assert environment_config.data_dir == DEFAULT_DATA_DIR


def test_data_dir(with_data_dir):
    environment_config = EnvironmentConfig(with_data_dir)
    assert environment_config.data_dir == "/test/data/dir"


def set_home_env(monkeypatch, tmpdir):
    monkeypatch.setenv("HOME", str(tmpdir))


def test_data_dir_abs_path_from_file(monkeypatch, tmpdir, with_data_dir_home):
    set_home_env(monkeypatch, tmpdir)

    config = EnvironmentConfig(with_data_dir_home)
    assert config.data_dir_abs_path == os.path.join(tmpdir, "data_dir")
