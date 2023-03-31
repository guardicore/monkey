import pytest
from itsdangerous import BadData, SignatureExpired
from tests.unit_tests.monkey_island.cc.services.authentication_service.token.conftest import (
    build_app,
)

from monkey_island.cc.services.authentication_service.token import TokenValidator
from monkey_island.cc.services.authentication_service.token.token_generator import TokenGenerator


def test_validate_token__valid(freezer):
    token_expiration_timedelta = 1 * 60  # 1 minute
    generation_time = "2020-01-01 00:00:00"
    validation_time = "2020-01-01 00:00:30"
    payload = "fake_user_id"

    app, _ = build_app()
    token_generator = TokenGenerator(app.security)
    freezer.move_to(generation_time)
    token = token_generator.generate_token(payload)
    token_validator = TokenValidator(app.security, token_expiration_timedelta)
    freezer.move_to(validation_time)

    token_validator.validate_token(token)


def test_validate_token__old_token_invalid_on_new_token_generated():
    token_expiration_timedelta = 1 * 60  # 1 minute
    payload = "fake_user_id"

    app, _ = build_app()
    token_generator = TokenGenerator(app.security)
    token_validator = TokenValidator(app.security, token_expiration_timedelta)

    token_1 = token_generator.generate_token(payload)
    token_validator.validate_token(token_1)

    token_2 = token_generator.generate_token(payload)
    token_validator.validate_token(token_2)

    with pytest.raises(SignatureExpired):
        # this is still valid according to the expiration time but since
        # a new refresh token has been generated, it should be invalid
        token_validator.validate_token(token_1)


def test_validate_refresh_token__expired(freezer):
    token_expiration = 1 * 60  # 1 minute
    generation_time = "2020-01-01 00:00:00"
    validation_time = "2020-01-01 00:03:30"
    payload = "fake_user_id"

    app, _ = build_app()
    token_generator = TokenGenerator(app.security)
    freezer.move_to(generation_time)
    token = token_generator.generate_token(payload)
    token_validator = TokenValidator(app.security, token_expiration)
    freezer.move_to(validation_time)

    with pytest.raises(SignatureExpired):
        token_validator.validate_token(token)


def test_validate_refresh_token__invalid():
    token_expiration = 1 * 60  # 1 minute
    invalid_token = "invalid_token"

    app, _ = build_app()
    token_validator = TokenValidator(app.security, token_expiration)

    with pytest.raises(BadData):
        token_validator.validate_token(invalid_token)


def test_get_token_payload():
    token_expiration_timedelta = 1 * 60  # 1 minute
    payload = "fake_user_id"

    app, _ = build_app()
    token_generator = TokenGenerator(app.security)
    token_validator = TokenValidator(app.security, token_expiration_timedelta)

    token = token_generator.generate_token(payload)

    assert token_validator.get_token_payload(token) == payload


def test_get_token_payload__expired_token(freezer):
    token_expiration = 1 * 60  # 1 minute
    generation_time = "2020-01-01 00:00:00"
    validation_time = "2020-01-01 00:03:30"
    payload = "fake_user_id"

    app, _ = build_app()
    token_generator = TokenGenerator(app.security)
    freezer.move_to(generation_time)
    token = token_generator.generate_token(payload)
    token_validator = TokenValidator(app.security, token_expiration)
    freezer.move_to(validation_time)

    with pytest.raises(SignatureExpired):
        token_validator.get_token_payload(token)


def test_get_token_payload__invalid_token():
    token_expiration = 1 * 60  # 1 minute
    invalid_token = "invalid_token"

    app, _ = build_app()
    token_validator = TokenValidator(app.security, token_expiration)

    with pytest.raises(BadData):
        token_validator.get_token_payload(invalid_token)
