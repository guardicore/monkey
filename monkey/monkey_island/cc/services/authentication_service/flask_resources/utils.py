import json
from functools import wraps
from typing import Tuple

from flask import Request, request
from werkzeug.datastructures import ImmutableMultiDict


def get_username_password_from_request(_request: Request) -> Tuple[str, str]:
    """
    Deserialize the JSON binary data from the request and get the plaintext
    username and password.

    :param _request: A Flask Request object
    :raises JSONDecodeError: If invalid JSON data is provided
    """
    cred_dict = json.loads(request.data)
    username = cred_dict.get("username", "")
    password = cred_dict.get("password", "")
    return username, password


def include_auth_token(func):
    """
    A decorator that ensures that flask-security-too response includes an authentication token
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        http_args = request.args.to_dict()
        http_args["include_auth_token"] = ""

        request.args = ImmutableMultiDict(http_args)

        return func(*args, **kwargs)

    return decorated_function
