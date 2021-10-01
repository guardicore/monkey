import atexit
import json
import logging
import sys
from pathlib import Path
from threading import Thread
from typing import Tuple

import gevent.hub
from gevent.pywsgi import WSGIServer

# Add the monkey_island directory to the path, to make sure imports that don't start with
# "monkey_island." work.
from monkey_island.cc.server_utils.encryption import initialize_encryptor_factory

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
from monkey_island.cc.server_utils.consts import (  # noqa: E402
    GEVENT_EXCEPTION_LOG,
    MONGO_CONNECTION_TIMEOUT,
)
from monkey_island.cc.server_utils.island_logger import reset_logger, setup_logging  # noqa: E402
from monkey_island.cc.services.initialize import initialize_services  # noqa: E402
from monkey_island.cc.services.reporting.exporter_init import populate_exporter_list  # noqa: E402
from monkey_island.cc.services.utils.network_utils import local_ip_addresses  # noqa: E402
from monkey_island.cc.setup import island_config_options_validator  # noqa: E402
from monkey_island.cc.setup.gevent_hub_error_handler import GeventHubErrorHandler  # noqa: E402
from monkey_island.cc.setup.island_config_options import IslandConfigOptions  # noqa: E402
from monkey_island.cc.setup.mongo import mongo_setup  # noqa: E402
from monkey_island.cc.setup.mongo.mongo_db_process import MongoDbProcess  # noqa: E402

logger = logging.getLogger(__name__)


def run_monkey_island():
    island_args = parse_cli_args()
    config_options, server_config_path = _setup_data_dir(island_args)

    _exit_on_invalid_config_options(config_options)

    _configure_logging(config_options)
    _initialize_globals(config_options, server_config_path)

    mongo_db_process = None
    if config_options.start_mongodb:
        mongo_db_process = _start_mongodb(config_options.data_dir)

    _connect_to_mongodb(mongo_db_process)

    _configure_gevent_exception_handling(Path(config_options.data_dir))
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


def _exit_on_invalid_config_options(config_options: IslandConfigOptions):
    try:
        island_config_options_validator.raise_on_invalid_options(config_options)
    except Exception as ex:
        print(f"Configuration error: {ex}")
        exit(1)


def _configure_logging(config_options):
    reset_logger()
    setup_logging(config_options.data_dir, config_options.log_level)


def _initialize_globals(config_options: IslandConfigOptions, server_config_path: str):
    env_singleton.initialize_from_file(server_config_path)

    initialize_encryptor_factory(config_options.data_dir)
    initialize_services(config_options.data_dir)


def _start_mongodb(data_dir: Path) -> MongoDbProcess:
    mongo_db_process = mongo_setup.start_mongodb(data_dir)
    mongo_setup.register_mongo_shutdown_callback(mongo_db_process)

    return mongo_db_process


def _connect_to_mongodb(mongo_db_process: MongoDbProcess):
    try:
        mongo_setup.connect_to_mongodb(MONGO_CONNECTION_TIMEOUT)
    except mongo_setup.MongoDBTimeOutError as ex:
        if mongo_db_process and not mongo_db_process.is_running():
            logger.error(
                f"Failed to start MongoDB process. Check log at {mongo_db_process.log_file}."
            )
        else:
            logger.error(ex)
        sys.exit(1)
    except mongo_setup.MongoDBVersionError as ex:
        logger.error(ex)
        sys.exit(1)


def _configure_gevent_exception_handling(data_dir):
    hub = gevent.hub.get_hub()

    gevent_exception_log = open(data_dir / GEVENT_EXCEPTION_LOG, "w+", buffering=1)
    atexit.register(gevent_exception_log.close)

    # Send gevent's exception output to a log file.
    # https://www.gevent.org/api/gevent.hub.html#gevent.hub.Hub.exception_stream
    hub.exception_stream = gevent_exception_log
    hub.handle_error = GeventHubErrorHandler(hub, logger)


def _start_island_server(should_setup_only, config_options: IslandConfigOptions):
    populate_exporter_list()
    app = init_app(mongo_setup.MONGO_URL)

    if should_setup_only:
        logger.warning("Setup only flag passed. Exiting.")
        return

    bootloader_server_thread = _start_bootloader_server()

    logger.info(
        f"Using certificate path: {config_options.crt_path}, and key path: "
        f"{config_options.key_path}."
    )

    if env_singleton.env.is_debug():
        app.run(
            host="0.0.0.0",
            debug=True,
            ssl_context=(config_options.crt_path, config_options.key_path),
        )
    else:
        http_server = WSGIServer(
            ("0.0.0.0", env_singleton.env.get_island_port()),
            app,
            certfile=config_options.crt_path,
            keyfile=config_options.key_path,
            log=logger,
            error_log=logger,
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
