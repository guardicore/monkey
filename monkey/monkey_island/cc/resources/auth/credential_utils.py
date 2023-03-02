import json
from typing import Tuple

from flask import Request, request


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
