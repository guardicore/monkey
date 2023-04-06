import json
from copy import deepcopy
from functools import wraps
from typing import Tuple

from flask import Request, Response, request
from werkzeug.datastructures import ImmutableMultiDict

from common.common_consts.token_keys import EXPIRATION_TIME_KEY_NAME


def get_username_password_from_request(_request: Request) -> Tuple[str, str]:
    """
    Deserialize the JSON binary data from the request and get the plaintext
    username and password.

    :param _request: A Flask Request object
    :raises JSONDecodeError: If invalid JSON data is provided
    :raises KeyError: If username or password were not provided in the request
    """
    cred_dict = json.loads(request.data)

    username = cred_dict["username"]
    password = cred_dict["password"]

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


def add_expiration_time_to_response(response: Response, expiration_time_sec: int) -> Response:
    """
    Returns a new copy of the response with the expiration time added

    :param response: A Flask Response object
    :return: A new Flask Response object with the expiration time added
    """
    new_response = deepcopy(response)
    new_response_json = deepcopy(response.json)
    new_response_json["response"]["user"][EXPIRATION_TIME_KEY_NAME] = expiration_time_sec
    new_response.data = json.dumps(new_response_json).encode()

    return new_response
