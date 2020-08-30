import hashlib
import logging
import os
from abc import ABCMeta, abstractmethod
from datetime import timedelta

__author__ = 'itay.mizeretz'

from common.utils.exceptions import (AlreadyRegisteredError,
                                     CredentialsNotRequiredError,
                                     InvalidRegistrationCredentialsError)
from monkey_island.cc.environment.environment_config import EnvironmentConfig
from monkey_island.cc.environment.user_creds import UserCreds

logger = logging.getLogger(__name__)


class Environment(object, metaclass=ABCMeta):
    _ISLAND_PORT = 5000
    _MONGO_DB_NAME = "monkeyisland"
    _MONGO_DB_HOST = "localhost"
    _MONGO_DB_PORT = 27017
    _MONGO_URL = os.environ.get("MONKEY_MONGO_URL",
                                "mongodb://{0}:{1}/{2}".format(_MONGO_DB_HOST, _MONGO_DB_PORT, str(_MONGO_DB_NAME)))
    _DEBUG_SERVER = False
    _AUTH_EXPIRATION_TIME = timedelta(minutes=30)

    _testing = False

    def __init__(self, config: EnvironmentConfig):
        self._config = config
        self._testing = False  # Assume env is not for unit testing.

    @property
    @abstractmethod
    def _credentials_required(self) -> bool:
        pass

    @abstractmethod
    def get_auth_users(self):
        pass

    def needs_registration(self) -> bool:
        try:
            needs_registration = self._try_needs_registration()
            return needs_registration
        except (CredentialsNotRequiredError, AlreadyRegisteredError) as e:
            logger.info(e)
            return False

    def try_add_user(self, credentials: UserCreds):
        if not credentials:
            raise InvalidRegistrationCredentialsError("Missing part of credentials.")
        if self._try_needs_registration():
            self._config.add_user(credentials)
            logger.info(f"New user {credentials.username} registered!")

    def _try_needs_registration(self) -> bool:
        if not self._credentials_required:
            raise CredentialsNotRequiredError("Credentials are not required "
                                              "for current environment.")
        else:
            if self._is_registered():
                raise AlreadyRegisteredError("User has already been registered. "
                                             "Reset credentials or login.")
            return True

    def _is_registered(self) -> bool:
        return self._credentials_required and self._is_credentials_set_up()

    def _is_credentials_set_up(self) -> bool:
        if self._config and self._config.user_creds:
            return True
        else:
            return False

    @property
    def testing(self):
        return self._testing

    @testing.setter
    def testing(self, value):
        self._testing = value

    def save_config(self):
        self._config.save_to_file()

    def get_config(self) -> EnvironmentConfig:
        return self._config

    def get_island_port(self):
        return self._ISLAND_PORT

    def get_mongo_url(self):
        return self._MONGO_URL

    def is_debug(self):
        return self._DEBUG_SERVER

    def get_auth_expiration_time(self):
        return self._AUTH_EXPIRATION_TIME

    @staticmethod
    def hash_secret(secret):
        hash_obj = hashlib.sha3_512()
        hash_obj.update(secret.encode('utf-8'))
        return hash_obj.hexdigest()

    def get_deployment(self) -> str:
        deployment = 'unknown'
        if self._config and self._config.deployment:
            deployment = self._config.deployment
        return deployment

    def set_deployment(self, deployment: str):
        self._config.deployment = deployment

    @property
    def mongo_db_name(self):
        return self._MONGO_DB_NAME

    @property
    def mongo_db_host(self):
        return self._MONGO_DB_HOST

    @property
    def mongo_db_port(self):
        return self._MONGO_DB_PORT
