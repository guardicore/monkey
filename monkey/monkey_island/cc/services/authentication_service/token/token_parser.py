from flask_security import Security

from common.base_models import InfectionMonkeyBaseModel

from .types import Token


class ParsedToken(InfectionMonkeyBaseModel):
    raw_token: Token
    expiration_time: int
    user_uniquifier: str


class TokenValidationError(Exception):
    """Raise when an invalid token is encountered"""


class TokenParser:
    def __init__(self, security: Security, token_expiration: int):
        self._token_serializer = security.remember_token_serializer
        self._token_expiration = token_expiration  # in seconds

    def parse(self, token: Token) -> ParsedToken:
        """
        Parses a token and returns a data structure with its components

        :param token: The token to parse
        :return: The parsed token
        :raises TokenValidationError: If the token could not be parsed
        """
        try:
            return ParsedToken(
                raw_token=token,
                expiration_time=self._token_expiration,
                user_uniquifier=str(
                    self._token_serializer.loads(token, max_age=self._token_expiration)
                ),
            )
        except Exception:
            raise TokenValidationError("Token is invalid, could not parse")
