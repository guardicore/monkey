import pytest
from tests.unit_tests.monkey_island.cc.services.authentication_service.token.conftest import (
    build_app,
)

from monkey_island.cc.services.authentication_service.token import TokenGenerator, TokenParser
from monkey_island.cc.services.authentication_service.token.token_parser import TokenValidationError


def test_parse():
    token_expiration_timedelta = 1 * 60  # 1 minute
    payload = "fake_user_id"

    app, _ = build_app()
    token_generator = TokenGenerator(app.security)
    token_parser = TokenParser(app.security, token_expiration_timedelta)

    token = token_generator.generate_token(payload)
    parsed_token = token_parser.parse(token)

    assert parsed_token.token == token
    assert parsed_token.expiration_time == token_expiration_timedelta
    assert parsed_token.payload == payload


def test_parse__expired_token(freezer):
    token_expiration = 1 * 60  # 1 minute
    generation_time = "2020-01-01 00:00:00"
    validation_time = "2020-01-01 00:03:30"
    payload = "fake_user_id"

    app, _ = build_app()
    token_generator = TokenGenerator(app.security)
    freezer.move_to(generation_time)
    token = token_generator.generate_token(payload)
    token_parser = TokenParser(app.security, token_expiration)
    freezer.move_to(validation_time)

    with pytest.raises(TokenValidationError):
        token_parser.parse(token)


def test_parse__invalid_token():
    token_expiration = 1 * 60  # 1 minute
    invalid_token = "invalid_token"

    app, _ = build_app()
    token_parser = TokenParser(app.security, token_expiration)

    with pytest.raises(TokenValidationError):
        token_parser.parse(invalid_token)
