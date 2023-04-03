from flask_security import Security

from .types import Token


class TokenGenerator:
    def __init__(self, security: Security):
        self._token_serializer = security.remember_token_serializer

    def generate_token(self, payload: str) -> Token:
        """
        Generates a refresh token for a user
        :param payload: String that will be encoded in the token
        :return: A refresh token
        """
        refresh_token = self._token_serializer.dumps(payload)

        return refresh_token
