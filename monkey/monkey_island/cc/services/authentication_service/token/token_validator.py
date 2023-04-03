from flask_security import Security

from .types import Token


class TokenValidator:
    def __init__(self, security: Security, token_expiration: int):
        self._token_serializer = security.remember_token_serializer
        self._token_expiration = token_expiration  # in seconds

    def validate_token(self, token: Token):
        """
        Validates a token
        :param token: A token to validate
        :raises BadSignature: If the token is invalid
        :raises SignatureExpired: If the token has expired
        """
        self._token_serializer.loads(token, max_age=self._token_expiration)
