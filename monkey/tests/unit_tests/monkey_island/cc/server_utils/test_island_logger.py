import logging
import os

import pytest

import monkey_island.cc.server_utils.island_logger as island_logger


@pytest.fixture(autouse=True)
def reset_logger():
    yield

    island_logger.reset_logger()


def test_setup_logging_file_log_level_debug(tmpdir):
    DATA_DIR = tmpdir
    LOG_FILE = os.path.join(DATA_DIR, island_logger.ISLAND_LOG_FILENAME)
    LOG_LEVEL = "DEBUG"
    TEST_STRING = "Hello, Monkey! (File; Log level: debug)"

    island_logger.setup_logging(DATA_DIR, LOG_LEVEL)

    logger = logging.getLogger("TestLogger")
    logger.debug(TEST_STRING)

    assert os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "r") as f:
        line = f.readline()
        assert TEST_STRING in line


def test_setup_logging_file_log_level_info(tmpdir):
    DATA_DIR = tmpdir
    LOG_FILE = os.path.join(DATA_DIR, island_logger.ISLAND_LOG_FILENAME)
    LOG_LEVEL = "INFO"
    TEST_STRING = "Hello, Monkey! (File; Log level: info)"

    island_logger.setup_logging(DATA_DIR, LOG_LEVEL)

    logger = logging.getLogger("TestLogger")
    logger.debug(TEST_STRING)

    assert os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "r") as f:
        line = f.readline()
        assert TEST_STRING not in line


def test_setup_logging_console_log_level_debug(capsys, tmpdir):
    DATA_DIR = tmpdir
    LOG_LEVEL = "DEBUG"
    TEST_STRING = "Hello, Monkey! (Console; Log level: debug)"

    island_logger.setup_logging(DATA_DIR, LOG_LEVEL)

    logger = logging.getLogger("TestLogger")
    logger.debug(TEST_STRING)

    captured = capsys.readouterr()
    assert TEST_STRING in captured.out


def test_setup_logging_console_log_level_info(capsys, tmpdir):
    DATA_DIR = tmpdir
    LOG_LEVEL = "INFO"
    TEST_STRING = "Hello, Monkey! (Console; Log level: info)"

    island_logger.setup_logging(DATA_DIR, LOG_LEVEL)

    logger = logging.getLogger("TestLogger")
    logger.debug(TEST_STRING)

    captured = capsys.readouterr()
    assert TEST_STRING not in captured.out


def test_setup_logging_console_log_level_lower_case(capsys, tmpdir):
    DATA_DIR = tmpdir
    LOG_LEVEL = "debug"
    TEST_STRING = "Hello, Monkey! (Console; Log level: debug)"

    island_logger.setup_logging(DATA_DIR, LOG_LEVEL)

    logger = logging.getLogger("TestLogger")
    logger.debug(TEST_STRING)

    captured = capsys.readouterr()
    assert TEST_STRING in captured.out


def test_setup_defailt_failsafe_logging(capsys):
    TEST_STRING = "Hello, Monkey! (Console; Log level: debug)"

    island_logger.setup_default_failsafe_logging()
    logger = logging.getLogger("TestLogger")
    logger.debug(TEST_STRING)

    captured = capsys.readouterr()
    assert TEST_STRING in captured.out
    assert "DEBUG" in captured.out
