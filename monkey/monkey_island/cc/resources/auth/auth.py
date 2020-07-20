from functools import wraps

from flask import abort, current_app
from flask_jwt import JWT, JWTError, _jwt_required
from werkzeug.security import safe_str_cmp

import monkey_island.cc.environment.environment_singleton as env_singleton
import monkey_island.cc.resources.auth.user_store as user_store

__author__ = 'itay.mizeretz'


def init_jwt(app):
    user_store.UserStore.set_users(env_singleton.env.get_auth_users())

    def authenticate(username, secret):
        user = user_store.UserStore.username_table.get(username, None)
        if user and safe_str_cmp(user.secret.encode('utf-8'), secret.encode('utf-8')):
            return user

    def identity(payload):
        user_id = payload['identity']
        return user_store.UserStore.user_id_table.get(user_id, None)

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
