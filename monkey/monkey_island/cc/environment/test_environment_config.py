import json
import os
import shutil

import pytest

from monkey_island.cc.consts import DEFAULT_DATA_DIR, MONKEY_ISLAND_ABS_PATH
from monkey_island.cc.environment.environment_config import EnvironmentConfig
from monkey_island.cc.environment.user_creds import UserCreds

TEST_RESOURCES_DIR = os.path.join(
    MONKEY_ISLAND_ABS_PATH, "cc", "testing", "environment"
)

WITH_CREDENTIALS = os.path.join(
    TEST_RESOURCES_DIR, "server_config_with_credentials.json"
)
NO_CREDENTIALS = os.path.join(TEST_RESOURCES_DIR, "server_config_no_credentials.json")
PARTIAL_CREDENTIALS = os.path.join(
    TEST_RESOURCES_DIR, "server_config_partial_credentials.json"
)
STANDARD_WITH_CREDENTIALS = os.path.join(
    TEST_RESOURCES_DIR, "server_config_standard_with_credentials.json"
)
WITH_DATA_DIR = os.path.join(TEST_RESOURCES_DIR, "server_config_with_data_dir.json")
WITH_DATA_DIR_HOME = os.path.join(TEST_RESOURCES_DIR, "server_config_with_data_dir_home.json")


@pytest.fixture
def config_file(tmpdir):
    return os.path.join(tmpdir, "test_config.json")


def test_get_with_credentials():
    config_dict = EnvironmentConfig(WITH_CREDENTIALS).to_dict()

    assert len(config_dict.keys()) == 5
    assert config_dict["server_config"] == "password"
    assert config_dict["deployment"] == "develop"
    assert config_dict["user"] == "test"
    assert config_dict["password_hash"] == "abcdef"
    assert config_dict["data_dir"] == DEFAULT_DATA_DIR


def test_get_with_no_credentials():
    config_dict = EnvironmentConfig(NO_CREDENTIALS).to_dict()

    assert len(config_dict.keys()) == 3
    assert config_dict["server_config"] == "password"
    assert config_dict["deployment"] == "develop"
    assert config_dict["data_dir"] == DEFAULT_DATA_DIR


def test_get_with_partial_credentials():
    config_dict = EnvironmentConfig(PARTIAL_CREDENTIALS).to_dict()

    assert len(config_dict.keys()) == 4
    assert config_dict["server_config"] == "password"
    assert config_dict["deployment"] == "develop"
    assert config_dict["user"] == "test"
    assert config_dict["data_dir"] == DEFAULT_DATA_DIR


def test_save_to_file(config_file):
    shutil.copyfile(STANDARD_WITH_CREDENTIALS, config_file)

    environment_config = EnvironmentConfig(config_file)
    environment_config.aws = "test_aws"
    environment_config.save_to_file()

    with open(config_file, "r") as f:
        from_file = json.load(f)

    assert len(from_file.keys()) == 6
    assert from_file["server_config"] == "standard"
    assert from_file["deployment"] == "develop"
    assert from_file["user"] == "test"
    assert from_file["password_hash"] == "abcdef"
    assert from_file["aws"] == "test_aws"
    assert from_file["data_dir"] == DEFAULT_DATA_DIR


def test_add_user(config_file):
    new_user = "new_user"
    new_password_hash = "fedcba"
    new_user_creds = UserCreds(new_user, new_password_hash)

    shutil.copyfile(STANDARD_WITH_CREDENTIALS, config_file)

    environment_config = EnvironmentConfig(config_file)
    environment_config.add_user(new_user_creds)

    with open(config_file, "r") as f:
        from_file = json.load(f)

    assert len(from_file.keys()) == 5
    assert from_file["user"] == new_user
    assert from_file["password_hash"] == new_password_hash


def test_get_users():
    environment_config = EnvironmentConfig(STANDARD_WITH_CREDENTIALS)
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


def test_data_dir():
    environment_config = EnvironmentConfig(WITH_DATA_DIR)
    assert environment_config.data_dir == "/test/data/dir"


def set_home_env(monkeypatch, tmpdir):
    monkeypatch.setenv("HOME", str(tmpdir))


def test_data_dir_abs_path_from_file(monkeypatch, tmpdir):
    set_home_env(monkeypatch, tmpdir)

    config = EnvironmentConfig(WITH_DATA_DIR_HOME)
    assert config.data_dir_abs_path == os.path.join(tmpdir, "data_dir")
