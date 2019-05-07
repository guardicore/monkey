import abc
from datetime import timedelta
import os
from Crypto.Hash import SHA3_512

__author__ = 'itay.mizeretz'


class Environment(object):
    __metaclass__ = abc.ABCMeta

    _ISLAND_PORT = 5000
    _MONGO_DB_NAME = "monkeyisland"
    _MONGO_DB_HOST = "localhost"
    _MONGO_DB_PORT = 27017
    _MONGO_URL = os.environ.get("MONKEY_MONGO_URL", "mongodb://{0}:{1}/{2}".format(_MONGO_DB_HOST, _MONGO_DB_PORT, str(_MONGO_DB_NAME)))
    _DEBUG_SERVER = False
    _AUTH_EXPIRATION_TIME = timedelta(hours=1)
    _testing = False

    @property
    def testing(self):
        return self._testing

    @testing.setter
    def testing(self, value):
        self._testing = value

    def __init__(self):
        self.config = None
        self._testing = False  # Assume env is not for unit testing.

    def set_config(self, config):
        self.config = config

    def get_island_port(self):
        return self._ISLAND_PORT

    def get_mongo_url(self):
        return self._MONGO_URL

    def is_debug(self):
        return self._DEBUG_SERVER

    def get_auth_expiration_time(self):
        return self._AUTH_EXPIRATION_TIME

    def hash_secret(self, secret):
        h = SHA3_512.new()
        h.update(secret)
        return h.hexdigest()

    @abc.abstractmethod
    def get_auth_users(self):
        return

    @property
    def mongo_db_name(self):
        return self._MONGO_DB_NAME

    @property
    def mongo_db_host(self):
        return self._MONGO_DB_HOST

    @property
    def mongo_db_port(self):
        return self._MONGO_DB_PORT
