import abc
from datetime import timedelta
import os

__author__ = 'itay.mizeretz'


class Environment(object):
    __metaclass__ = abc.ABCMeta

    _ISLAND_PORT = 5000
    _MONGO_URL = os.environ.get("MONKEY_MONGO_URL", "mongodb://localhost:27017/monkeyisland")
    _DEBUG_SERVER = False
    _AUTH_EXPIRATION_TIME = timedelta(hours=1)

    def get_island_port(self):
        return self._ISLAND_PORT

    def get_mongo_url(self):
        return self._MONGO_URL

    def is_debug(self):
        return self._DEBUG_SERVER

    def get_auth_expiration_time(self):
        return self._AUTH_EXPIRATION_TIME

    @abc.abstractmethod
    def is_auth_enabled(self):
        return

    @abc.abstractmethod
    def get_auth_users(self):
        return
