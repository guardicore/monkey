import atexit
import logging
import os
import time
from pathlib import Path

from monkeytoolbox import create_secure_directory
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from monkey_island.cc.mongo_consts import MONGO_URL
from monkey_island.cc.setup.mongo.mongo_db_process import MongoDbProcess

DB_DIR_NAME = "db"
MONGO_LOG_FILENAME = "mongodb.log"

MINIMUM_MONGO_DB_VERSION_REQUIRED = "4.2.0"

logger = logging.getLogger(__name__)


def start_mongodb(data_dir: Path) -> MongoDbProcess:
    db_dir = _create_db_dir(data_dir)
    log_file = os.path.join(data_dir, MONGO_LOG_FILENAME)

    mongo_db_process = MongoDbProcess(db_dir=db_dir, log_file=log_file)
    mongo_db_process.start()

    return mongo_db_process


def _create_db_dir(db_dir_parent_path: Path) -> str:
    db_dir = db_dir_parent_path / DB_DIR_NAME
    logger.info(f"Database content directory: {db_dir}.")

    create_secure_directory(db_dir)
    return str(db_dir)


def register_mongo_shutdown_callback(mongo_db_process: MongoDbProcess):
    atexit.register(mongo_db_process.stop)


def connect_to_mongodb(timeout: float):
    _wait_for_mongo_db_server(MONGO_URL, timeout)
    _assert_mongo_db_version(MONGO_URL)


def _wait_for_mongo_db_server(mongo_url, timeout):
    start_time = time.time()

    while not _is_db_server_up(mongo_url):
        logger.info(f"Waiting for MongoDB server on {mongo_url}")

        if (time.time() - start_time) > timeout:
            raise MongoDBTimeOutError(f"Failed to connect to MongoDB after {timeout} seconds.")

        time.sleep(1)


def _is_db_server_up(mongo_url):
    client = MongoClient(mongo_url, serverSelectionTimeoutMS=100)
    try:
        client.server_info()
        return True
    except ServerSelectionTimeoutError:
        return False


def _assert_mongo_db_version(mongo_url):
    """
    Checks if the mongodb version is new enough for running the app.
    If the DB is too old, quits.
    :param mongo_url: URL to the mongo the Island will use
    """
    required_version = tuple(MINIMUM_MONGO_DB_VERSION_REQUIRED.split("."))
    server_version = _get_db_version(mongo_url)
    if server_version < required_version:
        raise MongoDBVersionError(
            f"Mongo DB version too old. {required_version} is required, but got {server_version}."
        )
    else:
        logger.info(f"Mongo DB version OK. Got {server_version}")


def _get_db_version(mongo_url):
    """
    Return the mongo db version
    :param mongo_url: Which mongo to check.
    :return: version as a tuple (e.g. `(u'4', u'0', u'8')`)
    """
    client = MongoClient(mongo_url, serverSelectionTimeoutMS=100)
    server_version = tuple(client.server_info()["version"].split("."))
    return server_version


class MongoDBTimeOutError(Exception):
    pass


class MongoDBVersionError(Exception):
    pass
