import json
import secrets
from pathlib import Path
from typing import Any, Dict

from common.utils.file_utils import open_new_securely_permissioned_file

SECRET_FILE_NAME = ".flask_security_configuration.json"


def generate_flask_security_configuration(data_dir: Path) -> Dict[str, Any]:
    SECRET_FILE_PATH = str(data_dir / SECRET_FILE_NAME)
    try:
        with open(SECRET_FILE_PATH, "r") as secret_file:
            return json.load(secret_file)
    except FileNotFoundError:
        with open_new_securely_permissioned_file(SECRET_FILE_PATH, "w") as secret_file:
            secret_key = secrets.token_urlsafe(32)
            password_salt = secrets.SystemRandom().getrandbits(128)

            security_options = {"secret_key": secret_key, "password_salt": password_salt}
            json.dump(security_options, secret_file)

            return security_options
