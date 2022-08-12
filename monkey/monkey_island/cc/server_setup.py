import atexit
import json
import logging
import sys
from pathlib import Path
from typing import Sequence, Tuple

import gevent.hub
import requests
from gevent.pywsgi import WSGIServer

from monkey_island.cc import Version
from monkey_island.cc.deployment import Deployment
from monkey_island.cc.server_utils.consts import ISLAND_PORT
from monkey_island.cc.setup.config_setup import get_server_config

# Add the monkey_island directory to the path, to make sure imports that don't start with
# "monkey_island." work.
MONKEY_ISLAND_DIR_BASE_PATH = str(Path(__file__).parent.parent)
if str(MONKEY_ISLAND_DIR_BASE_PATH) not in sys.path:
    sys.path.insert(0, MONKEY_ISLAND_DIR_BASE_PATH)

from common import DIContainer  # noqa: E402
from common.version import get_version  # noqa: E402
from monkey_island.cc.app import init_app  # noqa: E402
from monkey_island.cc.arg_parser import IslandCmdArgs  # noqa: E402
from monkey_island.cc.arg_parser import parse_cli_args  # noqa: E402
from monkey_island.cc.server_utils.consts import (  # noqa: E402
    GEVENT_EXCEPTION_LOG,
    MONGO_CONNECTION_TIMEOUT,
    MONKEY_ISLAND_ABS_PATH,
)
from monkey_island.cc.server_utils.island_logger import reset_logger, setup_logging  # noqa: E402
from monkey_island.cc.services.initialize import initialize_services  # noqa: E402
from monkey_island.cc.services.utils.network_utils import get_ip_addresses  # noqa: E402
from monkey_island.cc.setup import PyWSGILoggingFilter  # noqa: E402
from monkey_island.cc.setup import island_config_options_validator  # noqa: E402
from monkey_island.cc.setup.data_dir import IncompatibleDataDirectory, setup_data_dir  # noqa: E402
from monkey_island.cc.setup.gevent_hub_error_handler import GeventHubErrorHandler  # noqa: E402
from monkey_island.cc.setup.island_config_options import IslandConfigOptions  # noqa: E402
from monkey_island.cc.setup.mongo import mongo_setup  # noqa: E402
from monkey_island.cc.setup.mongo.mongo_db_process import MongoDbProcess  # noqa: E402

logger = logging.getLogger(__name__)


def run_monkey_island():
    island_args = parse_cli_args()
    config_options = _extract_config(island_args)
    _exit_on_invalid_config_options(config_options)

    _setup_data_dir(config_options.data_dir)
    _configure_logging(config_options)

    ip_addresses, deployment, version = _collect_system_info()

    _send_analytics(deployment, version)
    container = _initialize_di_container(ip_addresses, version, config_options.data_dir)

    _initialize_mongodb_connection(config_options.start_mongodb, config_options.data_dir)
    _start_island_server(island_args.setup_only, config_options, container)


def _extract_config(island_args: IslandCmdArgs) -> IslandConfigOptions:
    try:
        return get_server_config(island_args)
    except json.JSONDecodeError as err:
        print(f"Error loading server config: {err}")
        sys.exit(1)


def _setup_data_dir(data_dir_path: Path):
    try:
        setup_data_dir(data_dir_path)
    except IncompatibleDataDirectory as err:
        print(f"Incompatible data directory: {err}")
        sys.exit(1)


def _exit_on_invalid_config_options(config_options: IslandConfigOptions):
    try:
        island_config_options_validator.raise_on_invalid_options(config_options)
    except Exception as err:
        print(f"Configuration error: {err}")
        sys.exit(1)


def _configure_logging(config_options):
    reset_logger()
    setup_logging(config_options.data_dir, config_options.log_level)


def _collect_system_info() -> Tuple[Sequence[str], Deployment, Version]:
    deployment = _get_deployment()
    version = Version(get_version(), deployment)
    return (get_ip_addresses(), deployment, version)


def _get_deployment() -> Deployment:
    deployment_file_path = Path(MONKEY_ISLAND_ABS_PATH) / "cc" / "deployment.json"
    try:
        with open(deployment_file_path, "r") as deployment_info_file:
            deployment_info = json.load(deployment_info_file)
            return Deployment[deployment_info["deployment"].upper()]
    except KeyError as err:
        raise Exception(
            f"The deployment file ({deployment_file_path}) did not contain the expected data: "
            f"missing key {err}"
        )
    except Exception as err:
        raise Exception(f"Failed to fetch the deployment from {deployment_file_path}: {err}")


def _initialize_di_container(
    ip_addresses: Sequence[str], version: Version, data_dir: Path
) -> DIContainer:
    container = DIContainer()

    container.register_convention(Sequence[str], "ip_addresses", ip_addresses)
    container.register_instance(Version, version)
    container.register_convention(Path, "data_dir", data_dir)

    initialize_services(container, data_dir)

    return container


def _initialize_mongodb_connection(start_mongodb: bool, data_dir: Path):
    mongo_db_process = None
    if start_mongodb:
        mongo_db_process = _start_mongodb(data_dir)

    _connect_to_mongodb(mongo_db_process)


def _start_mongodb(data_dir: Path) -> MongoDbProcess:
    mongo_db_process = mongo_setup.start_mongodb(data_dir)
    mongo_setup.register_mongo_shutdown_callback(mongo_db_process)

    return mongo_db_process


def _connect_to_mongodb(mongo_db_process: MongoDbProcess):
    try:
        mongo_setup.connect_to_mongodb(MONGO_CONNECTION_TIMEOUT)
    except mongo_setup.MongoDBTimeOutError as err:
        if mongo_db_process and not mongo_db_process.is_running():
            logger.error(
                f"Failed to start MongoDB process. Check log at {mongo_db_process.log_file}."
            )
        else:
            logger.error(err)
        sys.exit(1)
    except mongo_setup.MongoDBVersionError as err:
        logger.error(err)
        sys.exit(1)


def _start_island_server(
    should_setup_only: bool, config_options: IslandConfigOptions, container: DIContainer
):
    _configure_gevent_exception_handling(config_options.data_dir)

    app = init_app(mongo_setup.MONGO_URL, container)

    if should_setup_only:
        logger.warning("Setup only flag passed. Exiting.")
        return

    logger.info(
        f"Using certificate path: {config_options.crt_path}, and key path: "
        f"{config_options.key_path}."
    )

    http_server = WSGIServer(
        ("0.0.0.0", ISLAND_PORT),
        app,
        certfile=config_options.crt_path,
        keyfile=config_options.key_path,
        log=_get_wsgi_server_logger(),
        error_log=logger,
    )
    _log_init_info()
    http_server.serve_forever()


def _configure_gevent_exception_handling(data_dir: Path):
    hub = gevent.hub.get_hub()

    gevent_exception_log = open(data_dir / GEVENT_EXCEPTION_LOG, "w+", buffering=1)
    atexit.register(gevent_exception_log.close)

    # Send gevent's exception output to a log file.
    # https://www.gevent.org/api/gevent.hub.html#gevent.hub.Hub.exception_stream
    hub.exception_stream = gevent_exception_log
    hub.handle_error = GeventHubErrorHandler(hub, logger)


def _get_wsgi_server_logger() -> logging.Logger:
    wsgi_server_logger = logger.getChild("wsgi")
    wsgi_server_logger.addFilter(PyWSGILoggingFilter())

    return wsgi_server_logger


def _log_init_info():
    logger.info("Monkey Island Server is running!")
    logger.info(f"version: {get_version()}")

    _log_web_interface_access_urls()


def _log_web_interface_access_urls():
    web_interface_urls = ", ".join([f"https://{ip}:{ISLAND_PORT}" for ip in get_ip_addresses()])
    logger.info(
        "To access the web interface, navigate to one of the the following URLs using your "
        f"browser: {web_interface_urls}"
    )


ANALYTICS_URL = (
    "https://m15mjynko3.execute-api.us-east-1.amazonaws.com/default?version={"
    "version}&deployment={deployment}"
)


def _send_analytics(deployment: Deployment, version: Version):
    url = ANALYTICS_URL.format(deployment=deployment.value, version=version.version_number)
    try:
        response = requests.get(url).json()
        logger.info(
            f"Version number and deployment type was sent to analytics server. "
            f"The response is: {response}"
        )
    except requests.exceptions.ConnectionError as err:
        logger.info(
            f"Failed to send deployment type and version number to the analytics server: {err}"
        )
