import json
from typing import Tuple

import bcrypt
from flask import Request, request

from monkey_island.cc.environment.user_creds import UserCreds


def hash_password(plaintext_password):
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(plaintext_password.encode("utf-8"), salt)

    return password_hash.decode()


def password_matches_hash(plaintext_password, password_hash):
    return bcrypt.checkpw(plaintext_password.encode("utf-8"), password_hash.encode("utf-8"))


def get_user_credentials_from_request(_request) -> UserCreds:
    username, password = get_creds_from_request(_request)
    password_hash = hash_password(password)

    return UserCreds(username, password_hash)


def get_secret_from_request(_request) -> str:
    username, password = get_creds_from_request(_request)
    return f"{username}:{password}"


def get_creds_from_request(_request: Request) -> Tuple[str, str]:
    cred_dict = json.loads(request.data)
    username = cred_dict.get("username", "")
    password = cred_dict.get("password", "")
    return username, password
