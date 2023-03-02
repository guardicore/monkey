import threading
from functools import wraps

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

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            with wrapper.lock:
                if wrapper.timer.is_expired():
                    wrapper.cached_value = fn(*args, **kwargs)
                    wrapper.timer.set(ttl)

            return wrapper.cached_value

        wrapper.cached_value = None
        wrapper.timer = EggTimer()
        wrapper.lock = threading.Lock()

        return wrapper

    return decorator
