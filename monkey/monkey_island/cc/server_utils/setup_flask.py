import secrets
from pathlib import Path

from common.utils.file_utils import open_new_securely_permissioned_file

SECRET_FILE_NAME = ".flask_secret"


def generate_flask_secret_key(data_dir: Path) -> str:
    SECRET_FILE_PATH = str(data_dir / SECRET_FILE_NAME)
    try:
        with open(SECRET_FILE_PATH, "r") as secret_file:
            return secret_file.read()
    except FileNotFoundError:
        with open_new_securely_permissioned_file(SECRET_FILE_PATH, "w") as secret_file:
            secret_key = secrets.token_urlsafe(32)
            secret_file.write(secret_key)

            return secret_key
