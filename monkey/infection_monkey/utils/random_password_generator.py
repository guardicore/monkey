import secrets


def get_random_password(length: int = 12) -> str:
    password = secrets.token_urlsafe(length)
    return password
