from functools import wraps

import flask_jwt
from flask_jwt import JWT
from werkzeug.security import safe_str_cmp

from cc.island_config import AUTH_ENABLED

__author__ = 'itay.mizeretz'


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id


users = [
    User(1, 'monkey', 'infection')
]
username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)


def init_jwt(app):
    if AUTH_ENABLED:
        JWT(app, authenticate, identity)


def jwt_required(realm=None):
    if AUTH_ENABLED:
        return flask_jwt.jwt_required(realm)
    else:
        def wrapper(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):
                return fn(*args, **kwargs)
            return decorator
        return wrapper
