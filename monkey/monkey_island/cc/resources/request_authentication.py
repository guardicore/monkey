import logging

import flask_jwt_extended

logger = logging.getLogger(__name__)


def create_access_token(username):
    access_token = flask_jwt_extended.create_access_token(identity=username)
    logger.debug(f"Created access token for user {username} that begins with {access_token[:4]}")

    return access_token
