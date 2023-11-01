import os
from pathlib import Path
from typing import Any

from monkey_island.cc.server_utils.consts import (
    DEFAULT_CRT_PATH,
    DEFAULT_DATA_DIR,
    DEFAULT_KEY_PATH,
    DEFAULT_LOG_LEVEL,
    DEFAULT_START_MONGO_DB,
)
from monkey_island.cc.setup.island_config_options import IslandConfigOptions

TEST_CONFIG_FILE_CONTENTS_SPECIFIED: dict[str, Any] = {
    "data_dir": "/tmp",
    "log_level": "test",
    "mongodb": {"start_mongodb": False},
    "ssl_certificate": {
        "ssl_certificate_file": "/tmp/test.crt",
        "ssl_certificate_key_file": "/tmp/test.key",
    },
}

TEST_CONFIG_FILE_CONTENTS_UNSPECIFIED: dict[str, Any] = {}

TEST_CONFIG_FILE_CONTENTS_NO_STARTMONGO: dict[str, Any] = {"mongodb": {}}


def test_data_dir_specified():
    assert_data_dir_equals(TEST_CONFIG_FILE_CONTENTS_SPECIFIED, "/tmp")


def test_data_dir_uses_default():
    assert_data_dir_equals(TEST_CONFIG_FILE_CONTENTS_UNSPECIFIED, DEFAULT_DATA_DIR)


def test_data_dir_expanduser(patched_home_env):
    DATA_DIR_NAME = "test_data_dir"

    assert_data_dir_equals(
        {"data_dir": os.path.join("~", DATA_DIR_NAME)},
        patched_home_env / DATA_DIR_NAME,
    )


def test_data_dir_expandvars(home_env_variable, patched_home_env):
    DATA_DIR_NAME = "test_data_dir"

    assert_data_dir_equals(
        {"data_dir": os.path.join(home_env_variable, DATA_DIR_NAME)},
        patched_home_env / DATA_DIR_NAME,
    )


def assert_data_dir_equals(config_file_contents, expected_data_dir):
    assert_island_config_option_equals(config_file_contents, "data_dir", Path(expected_data_dir))


def test_log_level():
    options = IslandConfigOptions(**TEST_CONFIG_FILE_CONTENTS_SPECIFIED)
    assert options.log_level == "test"
    options = IslandConfigOptions(**TEST_CONFIG_FILE_CONTENTS_UNSPECIFIED)
    assert options.log_level == DEFAULT_LOG_LEVEL


def test_mongodb():
    options = IslandConfigOptions(**TEST_CONFIG_FILE_CONTENTS_SPECIFIED)
    assert not options.mongodb.start_mongodb
    options = IslandConfigOptions(**TEST_CONFIG_FILE_CONTENTS_UNSPECIFIED)
    assert options.mongodb.start_mongodb == DEFAULT_START_MONGO_DB
    options = IslandConfigOptions(**TEST_CONFIG_FILE_CONTENTS_NO_STARTMONGO)
    assert options.mongodb.start_mongodb == DEFAULT_START_MONGO_DB


def test_crt_path_uses_default():
    assert_ssl_certificate_file_equals(TEST_CONFIG_FILE_CONTENTS_UNSPECIFIED, DEFAULT_CRT_PATH)


def test_crt_path_specified():
    assert_ssl_certificate_file_equals(
        TEST_CONFIG_FILE_CONTENTS_SPECIFIED,
        TEST_CONFIG_FILE_CONTENTS_SPECIFIED["ssl_certificate"]["ssl_certificate_file"],
    )


def test_crt_path_expanduser(patched_home_env):
    FILE_NAME = "test.crt"

    assert_ssl_certificate_file_equals(
        {"ssl_certificate": {"ssl_certificate_file": os.path.join("~", FILE_NAME)}},
        patched_home_env / FILE_NAME,
    )


def test_crt_path_expandvars(home_env_variable, patched_home_env):
    FILE_NAME = "test.crt"

    assert_ssl_certificate_file_equals(
        {"ssl_certificate": {"ssl_certificate_file": os.path.join(home_env_variable, FILE_NAME)}},
        patched_home_env / FILE_NAME,
    )


def assert_ssl_certificate_file_equals(config_file_contents, expected_ssl_certificate_file):
    options = IslandConfigOptions(**config_file_contents)
    assert options.ssl_certificate.ssl_certificate_file == Path(expected_ssl_certificate_file)


def test_key_path_uses_default():
    assert_ssl_certificate_key_file_equals(TEST_CONFIG_FILE_CONTENTS_UNSPECIFIED, DEFAULT_KEY_PATH)


def test_key_path_specified():
    assert_ssl_certificate_key_file_equals(
        TEST_CONFIG_FILE_CONTENTS_SPECIFIED,
        TEST_CONFIG_FILE_CONTENTS_SPECIFIED["ssl_certificate"]["ssl_certificate_key_file"],
    )


def test_key_path_expanduser(patched_home_env):
    FILE_NAME = "test.key"

    assert_ssl_certificate_key_file_equals(
        {"ssl_certificate": {"ssl_certificate_key_file": os.path.join("~", FILE_NAME)}},
        patched_home_env / FILE_NAME,
    )


def test_key_path_expandvars(home_env_variable, patched_home_env):
    FILE_NAME = "test.key"

    assert_ssl_certificate_key_file_equals(
        {
            "ssl_certificate": {
                "ssl_certificate_key_file": os.path.join(home_env_variable, FILE_NAME)
            }
        },
        patched_home_env / FILE_NAME,
    )


def assert_ssl_certificate_key_file_equals(config_file_contents, expected_ssl_certificate_file):
    options = IslandConfigOptions(**config_file_contents)
    assert options.ssl_certificate.ssl_certificate_key_file == Path(expected_ssl_certificate_file)


def assert_island_config_option_equals(config_file_contents, option_name, expected_value):
    options = IslandConfigOptions(**config_file_contents)
    assert getattr(options, option_name) == expected_value
