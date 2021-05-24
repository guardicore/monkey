from mongoengine import connect

# Needed so that a server_config.json file exists at the default path,
# otherwise, unit tests will error while importing `env_singleton` below.
from monkey_island.cc.environment import data_dir_generator, server_config_handler  # noqa: E402

from ..server_utils.consts import DEFAULT_DATA_DIR

data_dir_generator.create_data_dir(DEFAULT_DATA_DIR, False)
server_config_handler.create_default_server_config_file()

import monkey_island.cc.environment.environment_singleton as env_singleton  # noqa: E402

from .command_control_channel import CommandControlChannel  # noqa: F401, E402

# Order of importing matters here, for registering the embedded and referenced documents before
# using them.
from .config import Config  # noqa: F401, E402
from .creds import Creds  # noqa: F401, E402
from .monkey import Monkey  # noqa: F401, E402
from .monkey_ttl import MonkeyTtl  # noqa: F401, E402
from .pba_results import PbaResults  # noqa: F401, E402

connect(
    db=env_singleton.env.mongo_db_name,
    host=env_singleton.env.mongo_db_host,
    port=env_singleton.env.mongo_db_port,
)
