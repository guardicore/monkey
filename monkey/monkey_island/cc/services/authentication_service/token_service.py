from typing import Dict, TypeAlias

from flask_security import Security

TokenPair: TypeAlias = Dict[str, str]


class TokenService:
    def __init__(self, security: Security):
        self._token_serializer = security.remember_token_serializer
        self._refresh_token_expiration = (
            security.app.config["SECURITY_TOKEN_MAX_AGE"]
            + security.app.config["SECURITY_REFRESH_TOKEN_TIMEDELTA"]
        )

    def generate_token_pair(self, user_id: str) -> TokenPair:
        """
        Generates a refresh token for a user
        :param user_id: Identification string that will be encoded in the token
        :return: A refresh token
        """
        # This returns the same token because the timestamp and user_id are the same
        access_token = self._token_serializer.dumps(user_id)
        refresh_token = self._token_serializer.dumps(user_id)

        return {"access_token": access_token, "refresh_token": refresh_token}

    def refresh_tokens(self, refresh_token: str) -> TokenPair:
        """
        Refreshes an auth token
        :param refresh_token: A refresh token
        :return: A new token pair
        """
        user_id = self._token_serializer.loads(
            refresh_token, max_age=self._refresh_token_expiration
        )

        return self.generate_token_pair(user_id)
