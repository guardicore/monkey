from monkey_island.cc.server_utils.consts import DEFAULT_LOG_LEVEL, DEFAULT_START_MONGO_DB
from monkey_island.setup.island_config_options import IslandConfigOptions

TEST_CONFIG_FILE_CONTENTS_STANDARD = {"data_dir": "/tmp", "mongodb": {"start_mongodb": False}}

TEST_CONFIG_FILE_CONTENTS_NO_STARTMONGO = {"data_dir": "/tmp", "mongodb": {}}


def test_island_config_options__standard():
    options = IslandConfigOptions(TEST_CONFIG_FILE_CONTENTS_STANDARD)
    assert not options.start_mongodb
    assert options.data_dir == "/tmp"
    assert options.log_level == DEFAULT_LOG_LEVEL


def test_island_config_options__no_starmongo():
    options = IslandConfigOptions(TEST_CONFIG_FILE_CONTENTS_NO_STARTMONGO)
    assert options.start_mongodb == DEFAULT_START_MONGO_DB
