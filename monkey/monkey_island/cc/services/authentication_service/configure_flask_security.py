import json
import secrets
from pathlib import Path
from typing import Any, Dict

from flask.sessions import SecureCookieSessionInterface

from common.utils.file_utils import open_new_securely_permissioned_file

SECRET_FILE_NAME = ".flask_security_configuration.json"


def generate_flask_security_configuration(data_dir: Path) -> Dict[str, Any]:
    secret_file_path = str(data_dir / SECRET_FILE_NAME)
    try:
        with open(secret_file_path, "r") as secret_file:
            return json.load(secret_file)
    except FileNotFoundError:
        with open_new_securely_permissioned_file(secret_file_path, "w") as secret_file:
            secret_key = secrets.token_urlsafe(32)
            password_salt = str(secrets.SystemRandom().getrandbits(128))

            security_options = {"secret_key": secret_key, "password_salt": password_salt}
            json.dump(security_options, secret_file)

            return security_options


def disable_session_cookies() -> SecureCookieSessionInterface:
    class CustomSessionInterface(SecureCookieSessionInterface):
        """Prevent creating session from API requests."""

        def should_set_cookie(self, *args, **kwargs):
            return False

        def save_session(self, *args, **kwargs):
            return

    return CustomSessionInterface()
