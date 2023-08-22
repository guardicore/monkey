from http import HTTPStatus
from typing import Optional

from flask import Response, make_response


def make_response_to_invalid_request(message: Optional[str] = None) -> Response:
    if message is None:
        message = "Invalid request"

    return make_response(
        {"message": message},
        HTTPStatus.BAD_REQUEST,
    )
