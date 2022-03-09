import logging
from itertools import count
from threading import Event, Thread
from typing import Any, Callable, Iterable, Optional, Tuple

logger = logging.getLogger(__name__)


def run_worker_threads(
    target: Callable[..., None],
    name_prefix: Optional[str] = None,
    args: Tuple = (),
    num_workers: int = 2,
):
    worker_threads = []
    counter = run_worker_threads.counters.setdefault(name_prefix, count(start=1))
    for i in range(0, num_workers):
        name = None if name_prefix is None else f"{name_prefix}-{next(counter)}"
        t = create_daemon_thread(target=target, name=name, args=args)
        t.start()
        worker_threads.append(t)

    for t in worker_threads:
        t.join()


run_worker_threads.counters = {}


def create_daemon_thread(
    target: Callable[..., None], name: Optional[str] = None, args: Tuple = ()
) -> Thread:
    return Thread(target=target, name=name, args=args, daemon=True)


def interruptable_iter(
    iterator: Iterable, interrupt: Event, log_message: str = None, log_level: int = logging.DEBUG
) -> Any:
    """
    Wraps an iterator so that the iterator can be interrupted if the `interrupt` Event is set. This
    is a convinient way to make loops interruptable and avoids the need to add an `if` to each and
    every loop.
    :param Iterable iterator: An iterator that will be made interruptable.
    :param Event interrupt: A `threading.Event` that, if set, will prevent the remainder of the
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
