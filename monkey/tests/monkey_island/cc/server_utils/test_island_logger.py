import logging
import os

import pytest

from monkey_island.cc.server_utils.island_logger import json_setup_logging


@pytest.fixture()
def test_logger_config_path(resources_dir):
    return os.path.join(resources_dir, "logger_config.json")


# TODO move into monkey/monkey_island/cc/test_common/fixtures after rebase/backmerge
@pytest.fixture
def mock_home_env(monkeypatch, tmpdir):
    monkeypatch.setenv("HOME", str(tmpdir))


def test_expanduser_filename(mock_home_env, tmpdir, test_logger_config_path):
    INFO_LOG = os.path.join(tmpdir, "info.log")
    TEST_STRING = "Hello, Monkey!"

    json_setup_logging(test_logger_config_path)

    logger = logging.getLogger("TestLogger")
    logger.info(TEST_STRING)

    assert os.path.isfile(INFO_LOG)
    with open(INFO_LOG, "r") as f:
        line = f.readline()
        assert TEST_STRING in line
