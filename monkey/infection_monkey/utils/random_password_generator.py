import secrets

SECRET_BYTE_LENGTH = 32


def get_random_password(length: int = SECRET_BYTE_LENGTH) -> str:
    password = secrets.token_urlsafe(length)
    return password
