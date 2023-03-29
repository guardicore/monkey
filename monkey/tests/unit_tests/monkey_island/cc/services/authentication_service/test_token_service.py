from typing import Dict, Tuple

import pytest
from flask import Flask
from flask_restful import Api
from flask_security import Security
from itsdangerous import SignatureExpired
from tests.unit_tests.monkey_island.conftest import init_mock_app, init_mock_datastore

from monkey_island.cc.services.authentication_service import AccountRole
from monkey_island.cc.services.authentication_service.token_service import TokenService

USER_EMAIL = "unittest@me.com"


def build_app(auth_token_expiration, refresh_token_expiration) -> Tuple[Flask, Api]:
    app, api = init_mock_app()
    app.config["SECURITY_TOKEN_MAX_AGE"] = auth_token_expiration
    app.config["SECURITY_REFRESH_TOKEN_TIMEDELTA"] = refresh_token_expiration
    user_datastore = init_mock_datastore()

    island_role = user_datastore.find_or_create_role(name=AccountRole.ISLAND_INTERFACE.name)
    app.security = Security(app, user_datastore)
    ds = app.security.datastore
    with app.app_context():
        ds.create_user(email=USER_EMAIL, username="test", password="password", roles=[island_role])
        ds.commit()

    return app, api


def generate_token_pair(
    freezer,
    generation_time: str,
    payload: str,
    access_token_expiration=1 * 60,
    refresh_token_expiration=1 * 60,
) -> Tuple[Dict[str, str], TokenService]:
    app, _ = build_app(access_token_expiration, refresh_token_expiration)
    token_service = TokenService(app.security)
    freezer.move_to(generation_time)
    tokens = token_service.generate_token_pair(payload)
    freezer.move_to("2020-01-01 00:01:30")
    return tokens, token_service


def test_refresh_tokens(freezer):
    access_token_expiration = refresh_token_expiration = 1 * 60  # 1 minute
    generation_time = "2020-01-01 00:00:00"
    refresh_attempt_time = "2020-01-01 00:01:30"
    payload = "fake_user_id"
    # Since time and payload are static the token is static
    expected_token = "ImZha2VfdXNlcl9pZCI.XgvhWg._kbb1SATOQN6UySDQc9gO757oJc"

    tokens, token_service = generate_token_pair(
        freezer, generation_time, payload, access_token_expiration, refresh_token_expiration
    )
    freezer.move_to(refresh_attempt_time)

    new_tokens = token_service.refresh_tokens(tokens["refresh_token"])

    assert new_tokens != tokens
    assert new_tokens["access_token"] == expected_token


def test_refresh_tokens__expired(freezer):
    access_token_expiration = refresh_token_expiration = 1 * 60  # 1 minute
    generation_time = "2020-01-01 00:00:00"
    refresh_attempt_time = "2020-01-01 00:03:00"
    payload = "fake_user_id"

    tokens, token_service = generate_token_pair(
        freezer, generation_time, payload, access_token_expiration, refresh_token_expiration
    )
    freezer.move_to(refresh_attempt_time)

    with pytest.raises(SignatureExpired):
        token_service.refresh_tokens(tokens["refresh_token"])
