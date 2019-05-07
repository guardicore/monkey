from mongoengine import connect

# set up the DB connection.
from monkey_island.cc.environment.environment import env

if env.testing:
    connect('mongoenginetest', host='mongomock://localhost')
else:
    connect(db=env.mongo_db_name, host=env.mongo_db_host, port=env.mongo_db_port)

# Order or importing matters, for registering the embedded and referenced documents before using them.
from config import Config
from creds import Creds
from monkey_ttl import MonkeyTtl
from pba_results import PbaResults
from monkey import Monkey
