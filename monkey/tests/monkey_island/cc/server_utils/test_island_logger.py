import logging
import os

import pytest

from monkey_island.cc.server_utils.island_logger import setup_logging


# TODO move into monkey/monkey_island/cc/test_common/fixtures after rebase/backmerge
@pytest.fixture
def mock_home_env(monkeypatch, tmpdir):
    monkeypatch.setenv("HOME", str(tmpdir))


def test_expanduser_filename(mock_home_env, tmpdir):
    DATA_DIR = tmpdir
    INFO_LOG = os.path.join(DATA_DIR, "monkey_island.log")
    LOG_LEVEL = "DEBUG"
    TEST_STRING = "Hello, Monkey!"

    setup_logging(DATA_DIR, LOG_LEVEL)

    logger = logging.getLogger("TestLogger")
    logger.info(TEST_STRING)

    assert os.path.isfile(INFO_LOG)
    with open(INFO_LOG, "r") as f:
        line = f.readline()
        assert TEST_STRING in line
