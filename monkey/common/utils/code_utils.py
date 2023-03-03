import logging
import queue
import random
import secrets
import string
from threading import Event, Thread
from typing import Any, Callable, Dict, Iterable, List, MutableMapping, Optional, Type, TypeVar

T = TypeVar("T")

logger = logging.getLogger(__name__)


def apply_filters(iterable: Iterable[T], filters: Iterable[Callable[[T], bool]]) -> Iterable[T]:
    """
    Applies multiple filters to an iterable

    :param iterable: An iterable to be filtered
    :param filters: An iterable of filters to be applied to the iterable
    :return: A new iterable with the filters applied
    """
    filtered_iterable = iterable
    for f in filters:
        filtered_iterable = filter(f, filtered_iterable)

    return filtered_iterable


class Singleton(type):
    _instances: Dict[Type, type] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def queue_to_list(q: queue.Queue) -> List[Any]:
    list_ = []
    try:
        while True:
            list_.append(q.get_nowait())
    except queue.Empty:
        pass

    return list_


def del_key(mapping: MutableMapping[T, Any], key: T):
    """
    Delete a key from a mapping.

    Unlike the `del` keyword, this function does not raise a KeyError
    if the key does not exist.

    :param mapping: A mapping from which a key will be deleted
    :param key: A key to delete from `mapping`
    """
    mapping.pop(key, None)


def insecure_generate_random_string(
    n: int, character_set: str = string.ascii_letters + string.digits
) -> str:
    """
    Generate a random string

    This function generates a random string. The length is specified by the user. The character set
    can optionally be specified by the user.

    WARNING: This function is not safe to use for cryptographic purposes.

    :param n: The desired number of characters in the random string
    :param character set: The set of characters that may be included in the random string, defaults
                          to alphanumerics
    """
    return _generate_random_string(random.choices, n, character_set)  # noqa: DUO102


def secure_generate_random_string(
    n: int, character_set: str = string.ascii_letters + string.digits
) -> str:
    """
    Generate a random string

    This function generates a random string. The length is specified by the user. The character set
    can optionally be specified by the user.

    This function is safe to use for cryptographic purposes.

    WARNING: This function may block if the system does not have sufficient entropy.

    :param n: The desired number of characters in the random string
    :param character set: The set of characters that may be included in the random string, defaults
                          to alphanumerics
    """
    return _generate_random_string(secrets.SystemRandom().choices, n, character_set)


# Note: Trying to typehint the rng parameter is more trouble than it's worth
def _generate_random_string(rng, n: int, character_set: str) -> str:
    return "".join(rng(character_set, k=n))


class PeriodicCaller:
    """
    Periodically calls a function

    Given a callable and a period, this component calls the callback periodically. The calls can
    occur in the background by calling the `start()` method, or in the foreground by calling the
    `run()` method. Note that this component is susceptible to "timer creep". In other words, the
    callable is not called every `period` seconds. It is called `period` seconds after the last call
    completes. This prevents multiple calls to the callback occurring concurrently.
    """

    def __init__(self, callback: Callable[[], None], period: float, name: Optional[str] = None):
        """
        :param callback: A callable to be called periodically
        :param period: The time to wait between calls of `callback`.
        :param name: A human-readable name for this caller that will be used in debug logging
        """
        self._callback = callback
        self._period = period

        self._name = f"PeriodicCaller-{callback.__name__}" if name is None else name

        self._stop = Event()
        self._thread: Optional[Thread] = None

    def start(self):
        """
        Periodically call the callback in the background
        """
        logger.debug(f"Starting {self._name}")

        self._stop.clear()
        self._thread = Thread(daemon=True, name=self._name, target=self.run)
        self._thread.start()

    def run(self):
        """
        Periodically call the callback and block until `stop()` is called
        """
        logger.debug(f"Successfully started {self._name}")

        while not self._stop.is_set():
            self._callback()
            self._stop.wait(self._period)

        logger.debug(f"Successfully stopped {self._name}")

    def stop(self, timeout: Optional[float] = None):
        """
        Stop this component from making any further calls

        When the timeout argument is not present or None, the operation will block until the
        PeriodicCaller stops.

        :param timeout: The number of seconds to wait for this component to stop
        """
        logger.debug(f"Stopping {self._name}")

        self._stop.set()

        if self._thread is not None:
            self._thread.join(timeout=timeout)

            if self._thread.is_alive():
                logger.warning(f"Timed out waiting for {self._name} to stop")
