from flask_security import Security

from .token_generator import TokenType
from .types import Token


class TokenValidator:
    def __init__(self, security: Security, token_expiration: int):
        self._token_serializer = security.remember_token_serializer
        self._token_expiration = token_expiration  # in seconds

    def validate_token(self, token: Token, token_type: TokenType = TokenType.REFRESH):
        """
        Validates a token
        :param token: A token to validate
        :param token_type: The type of the token
        :raises BadSignature: If the token is invalid
        :raises SignatureExpired: If the token has expired
        """
        payload = self._token_serializer.loads(token, max_age=self._token_expiration)
        if payload["type"] != token_type:
            raise Exception("Invalid token type")

    def get_token_payload(self, token: Token) -> str:
        """
        Returns the payload of a token
        :param token: Token to get the payload of
        """
        return str(self._token_serializer.loads(token, max_age=self._token_expiration)["payload"])
