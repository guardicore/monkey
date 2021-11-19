import logging
from abc import ABCMeta, abstractmethod
from datetime import timedelta

from common.utils.exceptions import (
    AlreadyRegisteredError,
    InvalidRegistrationCredentialsError,
)
from monkey_island.cc.environment.environment_config import EnvironmentConfig

logger = logging.getLogger(__name__)


class Environment(object, metaclass=ABCMeta):
    _DEBUG_SERVER = False
    _AUTH_EXPIRATION_TIME = timedelta(minutes=30)

    _testing = False

    def __init__(self, config: EnvironmentConfig):
        self._config = config
        self._testing = False  # Assume env is not for unit testing.

    @property
    def testing(self):
        return self._testing

    @testing.setter
    def testing(self, value):
        self._testing = value

    def get_config(self) -> EnvironmentConfig:
        return self._config

    def is_debug(self):
        return self._DEBUG_SERVER

    def get_auth_expiration_time(self):
        return self._AUTH_EXPIRATION_TIME
