import logging
import threading
from functools import wraps
from itertools import count
from threading import Lock, Thread
from typing import Any, Callable, Iterable, Iterator, Optional, Tuple, TypeVar

from monkeytypes import Event

logger = logging.getLogger(__name__)


def run_worker_threads(
    target: Callable[..., None],
    name_prefix: str,
    args: Tuple = (),
    num_workers: int = 2,
):
    worker_threads = []
    counter = run_worker_threads.counters.setdefault(name_prefix, count(start=1))
    for i in range(0, num_workers):
        name = f"{name_prefix}-{next(counter):02d}"
        t = create_daemon_thread(target=target, name=name, args=args)
        t.start()
        worker_threads.append(t)

    for t in worker_threads:
        t.join()


run_worker_threads.counters = {}


def create_daemon_thread(target: Callable[..., None], name: str, args: Tuple = ()) -> Thread:
    return Thread(target=target, name=name, args=args, daemon=True)


def interruptible_iter(
    iterator: Iterable,
    interrupt: Event,
    log_message: Optional[str] = None,
    log_level: int = logging.DEBUG,
) -> Any:
    """
    Wraps an iterator so that the iterator can be interrupted if the `interrupt` event is set. This
    is a convinient way to make loops interruptible and avoids the need to add an `if` to each and
    every loop.
    :param Iterable iterator: An iterator that will be made interruptible.
    :param Event interrupt: An `Event` that, if set, will prevent the remainder of the
                            iterator's items from being processed.
    :param str log_message: A message to be logged if the iterator is interrupted. If `log_message`
                            is `None` (default), then no message is logged.
    :param int log_level: The log level at which to log `log_message`, defaults to `logging.DEBUG`.
    """
    for i in iterator:
        if interrupt.is_set():
            if log_message:
                logger.log(log_level, log_message)

            break

        yield i


def interruptible_function(*, msg: Optional[str] = None, default_return_value: Any = None):
    """
    This decorator allows a function to be skipped if an interrupt (`Event`) is set. This is
    useful for interrupting running code without introducing duplicate `if` checks at the beginning
    of each function.

    Note: It is required that the decorated function accept a keyword-only argument named
    "interrupt".

    Example:
        def run_algorithm(*inputs, interrupt: Event):
            return_value = do_action_1(inputs[1], interrupt=interrupt)
            return_value = do_action_2(return_value + inputs[2], interrupt=interrupt)
            return_value = do_action_3(return_value + inputs[3], interrupt=interrupt)

            return return_value

        @interruptible_function(msg="Interrupt detected, skipping action 1", default_return_value=0)
        def do_action_1(input, *, interrupt: Event):
            # Process input
            ...

        @interruptible_function(msg="Interrupt detected, skipping action 2", default_return_value=0)
        def do_action_2(input, *, interrupt: Event):
            # Process input
            ...

        @interruptible_function(msg="Interrupt detected, skipping action 2", default_return_value=0)
        def do_action_2(input, *, interrupt: Event):
            # Process input
            ...

    :param str msg: A message to log at the debug level if an interrupt is detected. Defaults to
                    None.
    :param Any default_return_value: A value to return if the wrapped function is not run. Defaults
                                     to None.
    """

    def _decorator(fn):
        @wraps(fn)
        def _wrapper(*args, interrupt: Event, **kwargs):
            if interrupt.is_set():
                if msg:
                    logger.debug(msg)
                return default_return_value

            return fn(*args, interrupt=interrupt, **kwargs)

        return _wrapper

    return _decorator


class InterruptableThreadMixin:
    def __init__(self):
        self._interrupted = threading.Event()

    def stop(self):
        """Stop a running thread."""
        self._interrupted.set()


T = TypeVar("T")


class ThreadSafeIterator(Iterator[T]):
    """Provides a thread-safe iterator that wraps another iterator"""

    def __init__(self, iterator: Iterator[T]):
        self._lock = Lock()
        self._iterator = iterator

    def __next__(self) -> T:
        while True:
            with self._lock:
                return next(self._iterator)
