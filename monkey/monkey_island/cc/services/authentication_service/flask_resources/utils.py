import json
from copy import deepcopy
from functools import wraps
from typing import Tuple

from flask import Request, Response, request
from werkzeug.datastructures import ImmutableMultiDict

from monkey_island.cc.services.authentication_service.token import Token


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


REFRESH_TOKEN_KEY_NAME = "refresh_token"


def add_refresh_token_to_response(response: Response, refresh_token: Token) -> Response:
    """
    Returns a copy of the response object with the refresh token added to it

    :param response: A Flask Response object
    :param refresh_token: Refresh token to add to the response
    :return: A Flask Response object
    """
    new_data = deepcopy(response.json)
    new_data["response"]["user"][REFRESH_TOKEN_KEY_NAME] = refresh_token
    response.data = json.dumps(new_data).encode()
    return response
