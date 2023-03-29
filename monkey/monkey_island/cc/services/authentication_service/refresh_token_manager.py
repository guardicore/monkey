from typing import TypeAlias

from flask_security import Security

RefreshToken: TypeAlias = str


class RefreshTokenManager:
    def __init__(self, security: Security):
        self._token_serializer = security.remember_token_serializer
        self._refresh_token_expiration = (
            security.app.config["SECURITY_TOKEN_MAX_AGE"]
            + security.app.config["SECURITY_REFRESH_TOKEN_TIMEDELTA"]
        )

    def generate_refresh_token(self, payload: str) -> RefreshToken:
        """
        Generates a refresh token for a user
        :param payload: String that will be encoded in the token
        :return: A refresh token
        """
        refresh_token = self._token_serializer.dumps(payload)

        return refresh_token

    def validate_refresh_token(self, refresh_token: str):
        """
        Validates a refresh token
        :param refresh_token: A refresh token to validate
        """
        self._token_serializer.loads(refresh_token, max_age=self._refresh_token_expiration)
