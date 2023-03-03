import pytest
from tests.unit_tests.monkey_island.conftest import init_mock_security_app


@pytest.fixture(scope="function")
def mock_flask_app():
    app, _ = init_mock_security_app()

    with app.app_context():
        yield app
