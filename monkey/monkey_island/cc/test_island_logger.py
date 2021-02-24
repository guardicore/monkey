import logging
import os

import pytest

from monkey_island.cc.consts import MONKEY_ISLAND_ABS_PATH
from monkey_island.cc.island_logger import json_setup_logging

TEST_LOGGER_CONFIG_PATH = os.path.join(
    MONKEY_ISLAND_ABS_PATH, "cc", "testing", "logger_config.json"
)


# TODO move into monkey/monkey_island/cc/test_common/fixtures after rebase/backmerge
@pytest.fixture
def mock_home_env(monkeypatch, tmpdir):
    monkeypatch.setenv("HOME", str(tmpdir))


def test_expanduser_filename(mock_home_env, tmpdir):
    INFO_LOG = os.path.join(tmpdir, "info.log")
    TEST_STRING = "Hello, Monkey!"

    json_setup_logging(TEST_LOGGER_CONFIG_PATH)

    logger = logging.getLogger("TestLogger")
    logger.info(TEST_STRING)

    assert os.path.isfile(INFO_LOG)
    with open(INFO_LOG, "r") as f:
        line = f.readline()
        assert TEST_STRING in line
