import queue
import time
from threading import Thread
from typing import Any, Callable, Dict, List, MutableMapping, Type, TypeVar

T = TypeVar("T")


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


class PeriodicCaller:
    """
    Periodically calls a function

    Given a callable and a period, this component calls the callback periodically. The calls can
    occur in the background by calling the `start()` method, or in the foreground by calling the
    `run()` method. Note that this component is susceptible to "timer creep". In other words, the
    callable is not called every `period` seconds. It is called `period` seconds after the last call
    completes. This prevents multiple calls to the callback occurring concurrently.
    """

    def __init__(self, callback: Callable[[], None], period: float):
        """
        :param callback: A callable to be called periodically
        :param period: The time to wait between calls of `callback`.
        """
        self._thread = Thread(
            daemon=True, name="PeriodicCaller-{callback.__name__}", target=self.run
        )
        self._callback = callback
        self._period = period

    def start(self):
        """
        Periodically call the callback in the background
        """
        self._thread.start()

    def run(self):
        """
        Periodically call the callback and block until `stop()` is called
        """
        while True:
            self._callback()
            time.sleep(self._period)
