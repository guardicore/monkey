from functools import wraps

from flask import current_app, abort
from flask_jwt import JWT, _jwt_required, JWTError
from werkzeug.security import safe_str_cmp

from monkey_island.cc.environment.environment import env

__author__ = 'itay.mizeretz'


class User(object):
    def __init__(self, user_id, username, secret):
        self.id = user_id
        self.username = username
        self.secret = secret

    def __str__(self):
        return "User(id='%s')" % self.id


def init_jwt(app):
    users = env.get_auth_users()
    username_table = {u.username: u for u in users}
    userid_table = {u.id: u for u in users}

    def authenticate(username, secret):
        user = username_table.get(username, None)
        if user and safe_str_cmp(user.secret.encode('utf-8'), secret.encode('utf-8')):
            return user

    def identity(payload):
        user_id = payload['identity']
        return userid_table.get(user_id, None)

    JWT(app, authenticate, identity)


def jwt_required(realm=None):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                _jwt_required(realm or current_app.config['JWT_DEFAULT_REALM'])
                return fn(*args, **kwargs)
            except JWTError:
                abort(401)

        return decorator

    return wrapper
