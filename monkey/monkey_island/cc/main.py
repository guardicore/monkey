from __future__ import print_function  # In python 2.7

import os
import os.path
import sys
import time
import logging

MINIMUM_MONGO_DB_VERSION_REQUIRED = "3.6.0"

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if BASE_PATH not in sys.path:
    sys.path.insert(0, BASE_PATH)

from monkey_island.cc.island_logger import json_setup_logging
from monkey_island.cc.consts import MONKEY_ISLAND_ABS_PATH
# This is here in order to catch EVERYTHING, some functions are being called on imports the log init needs to be on top.
json_setup_logging(default_path=os.path.join(MONKEY_ISLAND_ABS_PATH, 'cc', 'island_logger_default_config.json'),
                   default_level=logging.DEBUG)
logger = logging.getLogger(__name__)

from monkey_island.cc.app import init_app
from monkey_island.cc.exporter_init import populate_exporter_list
from monkey_island.cc.utils import local_ip_addresses
from monkey_island.cc.environment.environment import env
from monkey_island.cc.database import is_db_server_up, get_db_version


def main():
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    mongo_url = os.environ.get('MONGO_URL', env.get_mongo_url())
    wait_for_mongo_db_server(mongo_url)
    assert_mongo_db_version(mongo_url)

    populate_exporter_list()
    app = init_app(mongo_url)

    crt_path = os.path.join(MONKEY_ISLAND_ABS_PATH, 'cc', 'server.crt')
    key_path = os.path.join(MONKEY_ISLAND_ABS_PATH, 'cc', 'server.key')

    if env.is_debug():
        app.run(host='0.0.0.0', debug=True, ssl_context=(crt_path, key_path))
    else:
        http_server = HTTPServer(WSGIContainer(app),
                                 ssl_options={'certfile': os.environ.get('SERVER_CRT', crt_path),
                                              'keyfile': os.environ.get('SERVER_KEY', key_path)})
        http_server.listen(env.get_island_port())
        logger.info(
            'Monkey Island Server is running on https://{}:{}'.format(local_ip_addresses()[0], env.get_island_port()))

        IOLoop.instance().start()


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
