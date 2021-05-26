import logging
import os
import sys
from pathlib import Path
from threading import Thread

from gevent.pywsgi import WSGIServer

# Add the monkey_island directory to the path, to make sure imports that don't start with
# "monkey_island." work.
MONKEY_ISLAND_DIR_BASE_PATH = str(Path(__file__).parent.parent)
if str(MONKEY_ISLAND_DIR_BASE_PATH) not in sys.path:
    sys.path.insert(0, MONKEY_ISLAND_DIR_BASE_PATH)

import monkey_island.cc.environment.environment_singleton as env_singleton  # noqa: E402
from common.version import get_version  # noqa: E402
from monkey_island.cc.app import init_app  # noqa: E402
from monkey_island.cc.resources.monkey_download import MonkeyDownload  # noqa: E402
from monkey_island.cc.server_utils.bootloader_server import BootloaderHttpServer  # noqa: E402
from monkey_island.cc.server_utils.consts import MONKEY_ISLAND_ABS_PATH  # noqa: E402
from monkey_island.cc.server_utils.encryptor import initialize_encryptor  # noqa: E402
from monkey_island.cc.services.initialize import initialize_services  # noqa: E402
from monkey_island.cc.services.reporting.exporter_init import populate_exporter_list  # noqa: E402
from monkey_island.cc.services.utils.network_utils import local_ip_addresses  # noqa: E402
from monkey_island.cc.setup.mongo.database_initializer import init_collections  # noqa: E402
from monkey_island.cc.setup.mongo.mongo_setup import MONGO_URL, setup_mongodb  # noqa: E402
from monkey_island.setup.island_config_options import IslandConfigOptions  # noqa: E402

logger = logging.getLogger(__name__)


def setup_island(setup_only: bool, config_options: IslandConfigOptions, server_config_path: str):
    env_singleton.initialize_from_file(server_config_path)

    initialize_encryptor(config_options.data_dir)
    initialize_services(config_options.data_dir)

    bootloader_server_thread = Thread(
        target=BootloaderHttpServer(MONGO_URL).serve_forever, daemon=True
    )

    bootloader_server_thread.start()
    _start_island_server(setup_only, config_options)
    bootloader_server_thread.join()


def _start_island_server(should_setup_only, config_options: IslandConfigOptions):

    setup_mongodb(config_options)

    populate_exporter_list()
    app = init_app(MONGO_URL)

    crt_path = str(Path(MONKEY_ISLAND_ABS_PATH, "cc", "server.crt"))
    key_path = str(Path(MONKEY_ISLAND_ABS_PATH, "cc", "server.key"))

    init_collections()

    if should_setup_only:
        logger.warning("Setup only flag passed. Exiting.")
        return

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
