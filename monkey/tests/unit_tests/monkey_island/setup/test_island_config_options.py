from monkey_island.cc.server_utils.consts import (
    DEFAULT_DATA_DIR,
    DEFAULT_LOG_LEVEL,
    DEFAULT_START_MONGO_DB,
)
from monkey_island.setup.island_config_options import IslandConfigOptions

TEST_CONFIG_FILE_CONTENTS_SPECIFIED = {
    "data_dir": "/tmp",
    "log_level": "test",
    "mongodb": {"start_mongodb": False},
}

TEST_CONFIG_FILE_CONTENTS_UNSPECIFIED = {}

TEST_CONFIG_FILE_CONTENTS_NO_STARTMONGO = {"mongodb": {}}


def test_island_config_options__data_dir():
    options = IslandConfigOptions(TEST_CONFIG_FILE_CONTENTS_SPECIFIED)
    assert options.data_dir == "/tmp"
    options = IslandConfigOptions(TEST_CONFIG_FILE_CONTENTS_UNSPECIFIED)
    assert options.data_dir == DEFAULT_DATA_DIR


def test_island_config_options__log_level():
    options = IslandConfigOptions(TEST_CONFIG_FILE_CONTENTS_SPECIFIED)
    assert options.log_level == "test"
    options = IslandConfigOptions(TEST_CONFIG_FILE_CONTENTS_UNSPECIFIED)
    assert options.log_level == DEFAULT_LOG_LEVEL


def test_island_config_options__mongodb():
    options = IslandConfigOptions(TEST_CONFIG_FILE_CONTENTS_SPECIFIED)
    assert not options.start_mongodb
    options = IslandConfigOptions(TEST_CONFIG_FILE_CONTENTS_UNSPECIFIED)
    assert options.start_mongodb == DEFAULT_START_MONGO_DB
    options = IslandConfigOptions(TEST_CONFIG_FILE_CONTENTS_NO_STARTMONGO)
    assert options.start_mongodb == DEFAULT_START_MONGO_DB
