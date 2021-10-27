import secrets
import string

SECRET_LENGTH = 32


def get_random_password(length: int = SECRET_LENGTH) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(alphabet) for i in range(length))
    return password
