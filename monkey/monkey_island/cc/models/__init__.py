from mongoengine import connect

from monkey_island.cc.environment.environment import env

# This section sets up the DB connection according to the environment.
#   If testing, use mongomock which only emulates mongo. for more information, see
#   http://docs.mongoengine.org/guide/mongomock.html .
#   Otherwise, use an actual mongod instance with connection parameters supplied by env.
if env.testing:
    connect('mongoenginetest', host='mongomock://localhost')
else:
    connect(db=env.mongo_db_name, host=env.mongo_db_host, port=env.mongo_db_port)

# Order of importing matters here, for registering the embedded and referenced documents before using them.
from config import Config
from creds import Creds
from monkey_ttl import MonkeyTtl
from pba_results import PbaResults
from monkey import Monkey
