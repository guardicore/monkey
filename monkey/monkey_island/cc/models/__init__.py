from mongoengine import connect

import monkey_island.cc.environment.environment_singleton as env_singleton  # noqa: E402

from .command_control_channel import CommandControlChannel  # noqa: F401, E402

# Order of importing matters here, for registering the embedded and referenced documents before
# using them.
from .config import Config  # noqa: F401, E402
from .creds import Creds  # noqa: F401, E402
from .monkey import Monkey  # noqa: F401, E402
from .monkey_ttl import MonkeyTtl  # noqa: F401, E402
from .pba_results import PbaResults  # noqa: F401, E402

# TODO refactor into explicit call when implementing mongodb startup
connect(
    db=env_singleton.env.mongo_db_name,
    host=env_singleton.env.mongo_db_host,
    port=env_singleton.env.mongo_db_port,
)
