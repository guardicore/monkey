from functools import wraps

from flask import current_app, abort
from flask_jwt import JWT, _jwt_required, JWTError
from werkzeug.security import safe_str_cmp

from cc.environment.environment import env

__author__ = 'itay.mizeretz'


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id


def init_jwt(app):
    users = env.get_auth_users()
    username_table = {u.username: u for u in users}
    userid_table = {u.id: u for u in users}

    def authenticate(username, password):
        user = username_table.get(username, None)
        if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
            return user

    def identity(payload):
        user_id = payload['identity']
        return userid_table.get(user_id, None)

    if env.is_auth_enabled():
        JWT(app, authenticate, identity)


def jwt_required(realm=None):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if env.is_auth_enabled():
                try:
                    _jwt_required(realm or current_app.config['JWT_DEFAULT_REALM'])
                except JWTError:
                    abort(401)
            return fn(*args, **kwargs)

        return decorator

    return wrapper
