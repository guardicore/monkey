import os

MONGO_DB_NAME = "monkey_island"
MONGO_DB_HOST = "localhost"
MONGO_DB_PORT = 27017
MONGO_URL = os.environ.get(
    "MONKEY_MONGO_URL",
    "mongodb://{0}:{1}/{2}".format(MONGO_DB_HOST, MONGO_DB_PORT, MONGO_DB_NAME),
)
