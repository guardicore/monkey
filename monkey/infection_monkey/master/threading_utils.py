from threading import Thread
from typing import Any, Callable, Tuple


def create_daemon_thread(target: Callable[[Any], None], args: Tuple[Any] = ()):
    return Thread(target=target, args=args, daemon=True)
