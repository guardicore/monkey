import logging
import os
import sys
import time

from monkey_island.cc.database import get_db_version, is_db_server_up
from monkey_island.cc.setup.mongo import mongo_connector
from monkey_island.cc.setup.mongo.mongo_connector import MONGO_DB_HOST, MONGO_DB_NAME, MONGO_DB_PORT
from monkey_island.cc.setup.mongo.mongo_db_process import MongoDbProcess
from monkey_island.setup.island_config_options import IslandConfigOptions

MONGO_URL = os.environ.get(
    "MONKEY_MONGO_URL",
    "mongodb://{0}:{1}/{2}".format(MONGO_DB_HOST, MONGO_DB_PORT, MONGO_DB_NAME),
)
MINIMUM_MONGO_DB_VERSION_REQUIRED = "4.2.0"

logger = logging.getLogger(__name__)


def start_mongodb(config_options: IslandConfigOptions):
    if config_options.start_mongodb:
        MongoDbProcess(
            db_dir_parent_path=config_options.data_dir, logging_dir_path=config_options.data_dir
        ).launch_mongodb()
    wait_for_mongo_db_server(MONGO_URL)
    assert_mongo_db_version(MONGO_URL)
    mongo_connector.connect_dal_to_mongodb()


def wait_for_mongo_db_server(mongo_url):
    while not is_db_server_up(mongo_url):
        logger.info("Waiting for MongoDB server on {0}".format(mongo_url))
        time.sleep(1)


def assert_mongo_db_version(mongo_url):
    """
    Checks if the mongodb version is new enough for running the app.
    If the DB is too old, quits.
    :param mongo_url: URL to the mongo the Island will use
    """
    required_version = tuple(MINIMUM_MONGO_DB_VERSION_REQUIRED.split("."))
    server_version = get_db_version(mongo_url)
    if server_version < required_version:
        logger.error(
            "Mongo DB version too old. {0} is required, but got {1}".format(
                str(required_version), str(server_version)
            )
        )
        sys.exit(-1)
    else:
        logger.info("Mongo DB version OK. Got {0}".format(str(server_version)))
