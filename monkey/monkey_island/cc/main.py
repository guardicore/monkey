import logging
import os
import sys
import time
from pathlib import Path
from threading import Thread

# Add the monkey_island directory to the path, to make sure imports that don't start with "monkey_island." work.
MONKEY_ISLAND_DIR_BASE_PATH = str(Path(__file__).parent.parent)
if str(MONKEY_ISLAND_DIR_BASE_PATH) not in sys.path:
    sys.path.insert(0, MONKEY_ISLAND_DIR_BASE_PATH)

from monkey_island.cc.consts import MONKEY_ISLAND_ABS_PATH  # noqa: E402
from monkey_island.cc.island_logger import json_setup_logging  # noqa: E402

# This is here in order to catch EVERYTHING, some functions are being called on imports the log init needs to be on top.
json_setup_logging(default_path=Path(MONKEY_ISLAND_ABS_PATH, 'cc', 'island_logger_default_config.json'),
                   default_level=logging.DEBUG)
logger = logging.getLogger(__name__)

import monkey_island.cc.environment.environment_singleton as env_singleton  # noqa: E402
from common.version import get_version  # noqa: E402
from monkey_island.cc.app import init_app  # noqa: E402
from monkey_island.cc.bootloader_server import \
    BootloaderHttpServer  # noqa: E402
from monkey_island.cc.database import get_db_version  # noqa: E402
from monkey_island.cc.database import is_db_server_up  # noqa: E402
from monkey_island.cc.network_utils import local_ip_addresses  # noqa: E402
from monkey_island.cc.resources.monkey_download import \
    MonkeyDownload  # noqa: E402
from monkey_island.cc.services.reporting.exporter_init import \
    populate_exporter_list  # noqa: E402
from monkey_island.cc.setup import setup  # noqa: E402

MINIMUM_MONGO_DB_VERSION_REQUIRED = "4.2.0"


def main(should_setup_only=False):
    logger.info("Starting bootloader server")
    mongo_url = os.environ.get('MONGO_URL', env_singleton.env.get_mongo_url())
    bootloader_server_thread = Thread(target=BootloaderHttpServer(mongo_url).serve_forever, daemon=True)

    bootloader_server_thread.start()
    start_island_server(should_setup_only)
    bootloader_server_thread.join()


def start_island_server(should_setup_only):
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop
    from tornado.wsgi import WSGIContainer

    mongo_url = os.environ.get('MONGO_URL', env_singleton.env.get_mongo_url())
    wait_for_mongo_db_server(mongo_url)
    assert_mongo_db_version(mongo_url)

    populate_exporter_list()
    app = init_app(mongo_url)

    crt_path = str(Path(MONKEY_ISLAND_ABS_PATH, 'cc', 'server.crt'))
    key_path = str(Path(MONKEY_ISLAND_ABS_PATH, 'cc', 'server.key'))

    setup()

    if should_setup_only:
        logger.warning("Setup only flag passed. Exiting.")
        return

    if env_singleton.env.is_debug():
        app.run(host='0.0.0.0', debug=True, ssl_context=(crt_path, key_path))
    else:
        http_server = HTTPServer(WSGIContainer(app),
                                 ssl_options={'certfile': os.environ.get('SERVER_CRT', crt_path),
                                              'keyfile': os.environ.get('SERVER_KEY', key_path)})
        http_server.listen(env_singleton.env.get_island_port())
        log_init_info()
        IOLoop.instance().start()


def log_init_info():
    logger.info('Monkey Island Server is running!')
    logger.info(f"version: {get_version()}")
    logger.info('Listening on the following URLs: {}'.format(
            ", ".join(["https://{}:{}".format(x, env_singleton.env.get_island_port()) for x in local_ip_addresses()])
        )
    )
    MonkeyDownload.log_executable_hashes()


def wait_for_mongo_db_server(mongo_url):
    while not is_db_server_up(mongo_url):
        logger.info('Waiting for MongoDB server on {0}'.format(mongo_url))
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
            'Mongo DB version too old. {0} is required, but got {1}'.format(str(required_version), str(server_version)))
        sys.exit(-1)
    else:
        logger.info('Mongo DB version OK. Got {0}'.format(str(server_version)))


if __name__ == '__main__':
    main()
