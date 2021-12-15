from threading import Thread
from typing import Callable, Tuple


def run_worker_threads(target: Callable[..., None], args: Tuple = (), num_workers: int = 2):
    worker_threads = []
    for i in range(0, num_workers):
        t = create_daemon_thread(target=target, args=args)
        t.start()
        worker_threads.append(t)

    for t in worker_threads:
        t.join()


def create_daemon_thread(target: Callable[..., None], args: Tuple = ()):
    return Thread(target=target, args=args, daemon=True)
