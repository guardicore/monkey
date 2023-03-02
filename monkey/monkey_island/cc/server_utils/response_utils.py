from http import HTTPStatus

from flask import Response, make_response


def bad_request_response() -> Response:
    return make_response(
        {"message": "Invalid request"},
        HTTPStatus.BAD_REQUEST,
    )
