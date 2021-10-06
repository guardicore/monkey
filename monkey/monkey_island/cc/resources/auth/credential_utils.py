import json
from typing import Tuple

import bcrypt
from flask import Request, request


def password_matches_hash(plaintext_password, password_hash):
    return bcrypt.checkpw(plaintext_password.encode("utf-8"), password_hash.encode("utf-8"))


def get_username_password_from_request(_request: Request) -> Tuple[str, str]:
    cred_dict = json.loads(request.data)
    username = cred_dict.get("username", "")
    password = cred_dict.get("password", "")
    return username, password
