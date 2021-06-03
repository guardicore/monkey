import json
import logging
import os
import sys
from pathlib import Path
from threading import Thread
from typing import Tuple

from gevent.pywsgi import WSGIServer

# Add the monkey_island directory to the path, to make sure imports that don't start with
# "monkey_island." work.
MONKEY_ISLAND_DIR_BASE_PATH = str(Path(__file__).parent.parent)
if str(MONKEY_ISLAND_DIR_BASE_PATH) not in sys.path:
    sys.path.insert(0, MONKEY_ISLAND_DIR_BASE_PATH)

import monkey_island.cc.environment.environment_singleton as env_singleton  # noqa: E402
import monkey_island.cc.setup.config_setup as config_setup  # noqa: E402
from common.version import get_version  # noqa: E402
from monkey_island.cc.app import init_app  # noqa: E402
from monkey_island.cc.arg_parser import IslandCmdArgs  # noqa: E402
from monkey_island.cc.arg_parser import parse_cli_args  # noqa: E402
from monkey_island.cc.resources.monkey_download import MonkeyDownload  # noqa: E402
from monkey_island.cc.server_utils.bootloader_server import BootloaderHttpServer  # noqa: E402
from monkey_island.cc.server_utils.consts import MONKEY_ISLAND_ABS_PATH  # noqa: E402
from monkey_island.cc.server_utils.encryptor import initialize_encryptor  # noqa: E402
from monkey_island.cc.server_utils.island_logger import reset_logger, setup_logging  # noqa: E402
from monkey_island.cc.services.initialize import initialize_services  # noqa: E402
from monkey_island.cc.services.reporting.exporter_init import populate_exporter_list  # noqa: E402
from monkey_island.cc.services.utils.network_utils import local_ip_addresses  # noqa: E402
from monkey_island.cc.setup.mongo.database_initializer import init_collections  # noqa: E402
from monkey_island.cc.setup.mongo.mongo_setup import (  # noqa: E402
    MONGO_URL,
    connect_to_mongodb,
    register_mongo_shutdown_callback,
    start_mongodb,
)
from monkey_island.setup.island_config_options import IslandConfigOptions  # noqa: E402

logger = logging.getLogger(__name__)


def run_monkey_island():
    island_args = parse_cli_args()
    config_options, server_config_path = _setup_data_dir(island_args)

    _configure_logging(config_options)
    _initialize_globals(config_options, server_config_path)

    if config_options.start_mongodb:
        mongo_db_process = start_mongodb(config_options.data_dir)
        register_mongo_shutdown_callback(mongo_db_process)

    connect_to_mongodb()

    _start_island_server(island_args.setup_only, config_options)


def _setup_data_dir(island_args: IslandCmdArgs) -> Tuple[IslandConfigOptions, str]:
    try:
        return config_setup.setup_data_dir(island_args)
    except OSError as ex:
        print(f"Error opening server config file: {ex}")
        exit(1)
    except json.JSONDecodeError as ex:
        print(f"Error loading server config: {ex}")
        exit(1)


def _configure_logging(config_options):
    reset_logger()
    setup_logging(config_options.data_dir, config_options.log_level)


def _initialize_globals(config_options: IslandConfigOptions, server_config_path: str):
    env_singleton.initialize_from_file(server_config_path)

    initialize_encryptor(config_options.data_dir)
    initialize_services(config_options.data_dir)


def _start_island_server(should_setup_only, config_options: IslandConfigOptions):
    populate_exporter_list()
    app = init_app(MONGO_URL)

    crt_path = str(Path(MONKEY_ISLAND_ABS_PATH, "cc", "server.crt"))
    key_path = str(Path(MONKEY_ISLAND_ABS_PATH, "cc", "server.key"))

    init_collections()

    if should_setup_only:
        logger.warning("Setup only flag passed. Exiting.")
        return

    bootloader_server_thread = _start_bootloader_server()

    if env_singleton.env.is_debug():
        app.run(host="0.0.0.0", debug=True, ssl_context=(crt_path, key_path))
    else:
        http_server = WSGIServer(
            ("0.0.0.0", env_singleton.env.get_island_port()),
            app,
            certfile=os.environ.get("SERVER_CRT", crt_path),
            keyfile=os.environ.get("SERVER_KEY", key_path),
        )
        _log_init_info()
        http_server.serve_forever()

    bootloader_server_thread.join()


def _start_bootloader_server() -> Thread:
    bootloader_server_thread = Thread(target=BootloaderHttpServer().serve_forever, daemon=True)

    bootloader_server_thread.start()

    return bootloader_server_thread


def _log_init_info():
    logger.info("Monkey Island Server is running!")
    logger.info(f"version: {get_version()}")
    logger.info(
        "Listening on the following URLs: {}".format(
            ", ".join(
                [
                    "https://{}:{}".format(x, env_singleton.env.get_island_port())
                    for x in local_ip_addresses()
                ]
            )
        )
    )
    MonkeyDownload.log_executable_hashes()
