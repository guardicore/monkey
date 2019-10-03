import logging
import abc

logger = logging.getLogger(__name__)


class AutoNewUser:
    """
    RAII object to use for creating and using a new user. Use with `with`.
    User will be created when the instance is instantiated.
    User will be available for use (log on for Windows, for example) at the start of the `with` scope.
    User will be removed (deactivated and deleted for Windows, for example) at the end of said `with` scope.

    Example:
             # Created                                                 # Logged on
        with AutoNewUser("user", "pass", is_on_windows()) as new_user:
            ...
            ...
        # Logged off and deleted
        ...
        """
    __metaclass__ = abc.ABCMeta

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @abc.abstractmethod
    def __enter__(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()

    @abc.abstractmethod
    def run_as(self, command):
        raise NotImplementedError()
