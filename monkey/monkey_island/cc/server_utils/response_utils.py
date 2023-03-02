from http import HTTPStatus

from flask import Response, make_response


def response_to_invalid_request() -> Response:
    return make_response(
        {"message": "Invalid request"},
        HTTPStatus.BAD_REQUEST,
    )
