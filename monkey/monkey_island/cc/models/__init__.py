from mongoengine import connect

import monkey_island.cc.environment.environment_singleton as env_singleton

from .command_control_channel import CommandControlChannel  # noqa: F401
# Order of importing matters here, for registering the embedded and referenced documents before using them.
from .config import Config  # noqa: F401
from .creds import Creds  # noqa: F401
from .monkey import Monkey  # noqa: F401
from .monkey_ttl import MonkeyTtl  # noqa: F401
from .pba_results import PbaResults  # noqa: F401

# This section sets up the DB connection according to the environment.
#   If testing, use mongomock which only emulates mongo. for more information, see
#   http://docs.mongoengine.org/guide/mongomock.html .
#   Otherwise, use an actual mongod instance with connection parameters supplied by env.
if env_singleton.env.testing:  # See monkey_island.cc.environment.testing
    connect('mongoenginetest', host='mongomock://localhost')
else:
    connect(db=env_singleton.env.mongo_db_name, host=env_singleton.env.mongo_db_host, port=env_singleton.env.mongo_db_port)
