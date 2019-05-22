import abc
from datetime import timedelta
import os
from Crypto.Hash import SHA3_512

__author__ = 'itay.mizeretz'


class Environment(object):
    __metaclass__ = abc.ABCMeta

    _ISLAND_PORT = 5000
    _MONGO_URL = os.environ.get("MONKEY_MONGO_URL", "mongodb://localhost:27017/monkeyisland")
    _DEBUG_SERVER = False
    _AUTH_EXPIRATION_TIME = timedelta(hours=1)
    _MONKEY_VERSION = "1.6.3"

    def __init__(self):
        self.config = None

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

    def get_deployment(self):
        return self._get_from_config('deployment', 'unknown')

    def is_develop(self):
        return self.get_deployment() == 'develop'

    def get_version(self):
        return self._MONKEY_VERSION + ('-dev' if self.is_develop() else '')

    def _get_from_config(self, key, default_value=None):
        val = default_value
        if self.config is not None:
            val = self.config.get(key, val)
        return val

    @abc.abstractmethod
    def get_auth_users(self):
        return
