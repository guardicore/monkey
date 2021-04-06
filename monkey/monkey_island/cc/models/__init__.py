from mongoengine import connect

import monkey_island.cc.environment.environment_singleton as env_singleton

from .command_control_channel import CommandControlChannel  # noqa: F401
# Order of importing matters here, for registering the embedded and referenced documents before using them.
from .config import Config  # noqa: F401
from .creds import Creds  # noqa: F401
from .monkey import Monkey  # noqa: F401
from .monkey_ttl import MonkeyTtl  # noqa: F401
from .pba_results import PbaResults  # noqa: F401

connect(db=env_singleton.env.mongo_db_name,
        host=env_singleton.env.mongo_db_host,
        port=env_singleton.env.mongo_db_port)
