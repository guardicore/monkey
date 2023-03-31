from enum import Enum

from flask_security import Security

from .types import Token


class TokenType(str, Enum):
    REFRESH = "refresh"


class TokenGenerator:
    def __init__(self, security: Security):
        self._token_serializer = security.remember_token_serializer

    def generate_token(self, payload: str, token_type=TokenType.REFRESH) -> Token:
        """
        Generates a refresh token for a user
        :param payload: String that will be encoded in the token
        :param token_type: The type of the token
        :return: A refresh token
        """
        _payload = {"payload": payload, "type": token_type}
        refresh_token = self._token_serializer.dumps(_payload)

        return refresh_token
