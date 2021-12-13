from threading import Thread
from typing import Callable, Tuple


def create_daemon_thread(target: Callable[..., None], args: Tuple = ()):
    return Thread(target=target, args=args, daemon=True)
