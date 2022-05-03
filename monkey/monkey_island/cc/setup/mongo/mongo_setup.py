import atexit
import logging
import os
import time
from pathlib import Path

from monkey_island.cc.database import get_db_version, is_db_server_up
from monkey_island.cc.server_utils.file_utils import create_secure_directory
from monkey_island.cc.setup.mongo import mongo_connector
from monkey_island.cc.setup.mongo.mongo_connector import MONGO_DB_HOST, MONGO_DB_NAME, MONGO_DB_PORT
from monkey_island.cc.setup.mongo.mongo_db_process import MongoDbProcess

DB_DIR_NAME = "db"
MONGO_LOG_FILENAME = "mongodb.log"
MONGO_URL = os.environ.get(
    "MONKEY_MONGO_URL",
    "mongodb://{0}:{1}/{2}".format(MONGO_DB_HOST, MONGO_DB_PORT, MONGO_DB_NAME),
)
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
    mongo_connector.connect_dal_to_mongodb()


def _wait_for_mongo_db_server(mongo_url, timeout):
    start_time = time.time()

    while not is_db_server_up(mongo_url):
        logger.info(f"Waiting for MongoDB server on {mongo_url}")

        if (time.time() - start_time) > timeout:
            raise MongoDBTimeOutError(f"Failed to connect to MongoDB after {timeout} seconds.")

        time.sleep(1)


def _assert_mongo_db_version(mongo_url):
    """
    Checks if the mongodb version is new enough for running the app.
    If the DB is too old, quits.
    :param mongo_url: URL to the mongo the Island will use
    """
    required_version = tuple(MINIMUM_MONGO_DB_VERSION_REQUIRED.split("."))
    server_version = get_db_version(mongo_url)
    if server_version < required_version:
        raise MongoDBVersionError(
            f"Mongo DB version too old. {required_version} is required, but got {server_version}."
        )
    else:
        logger.info(f"Mongo DB version OK. Got {server_version}")


class MongoDBTimeOutError(Exception):
    pass


class MongoDBVersionError(Exception):
    pass
