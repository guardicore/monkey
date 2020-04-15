from functools import wraps

from flask import request

from monkey_island.cc.models.test_telem import TestTelem

MONKEY_TELEM_COLLECTION_NAME = "monkey_telems_for_tests"


def store_test_telem(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        method = request.method
        content = request.data.decode()
        endpoint = str(request.url_rule)
        TestTelem(method=method, endpoint=endpoint, content=content).save()
        return f(*args, **kwargs)

    return decorated_function
