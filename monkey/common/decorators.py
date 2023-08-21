import threading
from functools import wraps
from typing import Any, Callable

from egg_timer import EggTimer


def request_cache(ttl: float):
    """
    This is a decorator that allows a single response of a function to be cached with an expiration
    time (TTL). The first call to the function is executed and the response is cached. Subsequent
    calls to the function result in the cached value being returned until the TTL elapses. Once the
    TTL elapses, the cache is considered stale and the decorated function will be called, its
    response cached, and the TTL reset.

    An example usage of this decorator is to wrap a function that makes frequent slow calls to an
    external resource, such as an HTTP request to a remote endpoint. If the most up-to-date
    information is not need, this decorator provides a simple way to cache the response for a
    certain amount of time.

    Example:
        @request_cache(600)
        def raining_outside():
            return requests.get(f"https://weather.service.api/check_for_rain/{MY_ZIP_CODE}")

    :param ttl: The time-to-live in seconds for the cached return value
    :return: The return value of the decorated function, or the cached return value if the TTL has
             not elapsed.
    """

    def decorator(fn: Callable) -> Callable:
        cached_value = None
        timer = EggTimer()
        lock = threading.Lock()

        @wraps(fn)
        def wrapper(*args, **kwargs) -> Any:
            nonlocal cached_value, timer, lock

            with lock:
                if timer.is_expired():
                    cached_value = fn(*args, **kwargs)
                    timer.set(ttl)

            return cached_value

        def clear_cache():
            nonlocal timer, lock

            with lock:
                timer.set(0)

        wrapper.clear_cache = clear_cache  # type: ignore [attr-defined]

        return wrapper

    return decorator
