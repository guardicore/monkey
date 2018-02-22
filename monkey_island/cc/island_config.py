from datetime import timedelta

__author__ = 'itay.mizeretz'

ISLAND_PORT = 5000
DEFAULT_MONGO_URL = "mongodb://localhost:27017/monkeyisland"
DEBUG_SERVER = False
AUTH_ENABLED = True
AUTH_EXPIRATION_TIME = timedelta(hours=1)
