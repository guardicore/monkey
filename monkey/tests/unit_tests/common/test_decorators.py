import time
from unittest.mock import MagicMock

from common.decorators import request_cache

TTL = 10


def test_request_cache(freezer):
    @request_cache(TTL)
    def make_request():
        return time.perf_counter_ns()

    # t=0
    t1 = make_request()
    freezer.tick()  # t=1
    t2 = make_request()

    freezer.tick(TTL)  # t=TTL+1

    t3 = make_request()
    t4 = make_request()

    assert t1 == t2
    assert t3 != t1
    assert t3 == t4


def test_request_cache__clear_cache(freezer):
    @request_cache(TTL)
    def make_request():
        return time.perf_counter_ns()

    # t=0
    t1 = make_request()
    freezer.tick()
    # t=1 -- Time has changed, but timer should not expire
    t2 = make_request()
    make_request.clear_cache()
    t3 = make_request()

    assert t1 == t2
    assert t1 != t3
