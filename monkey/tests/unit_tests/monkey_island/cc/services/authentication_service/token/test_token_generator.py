from tests.unit_tests.monkey_island.cc.services.authentication_service.token.conftest import (
    build_app,
)

from monkey_island.cc.services.authentication_service.token.token_generator import TokenGenerator


def test_generate_token(freezer):
    generation_time = "2020-01-01 00:00:00"
    payload = "fake_user_id"
    # Since time and payload are static the token is static
    expected_token = (
        "eyJwYXlsb2FkIjoiZmFrZV91c2VyX2lkIiwidHlwZSI6InJlZnJlc2gifQ."
        "XgvhAA.Gmy2VSpLaTjQCQ2EchjJbZsfIls"
    )

    app, _ = build_app()
    token_generator = TokenGenerator(app.security)
    freezer.move_to(generation_time)
    token = token_generator.generate_token(payload)

    assert token == expected_token
