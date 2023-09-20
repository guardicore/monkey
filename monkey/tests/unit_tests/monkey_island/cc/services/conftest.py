import pytest
from tests.unit_tests.monkey_island.conftest import init_mock_security_app


@pytest.fixture(scope="function")
def mock_flask_app():
    app, _ = init_mock_security_app()

    ds = app.security.datastore

    with app.app_context():
        inital_user = ds.find_user(email="unittest@me.com")
        if inital_user:
            ds.delete_user(inital_user)
            ds.commit()

        yield app
