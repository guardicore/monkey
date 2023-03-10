from unittest.mock import MagicMock

import pytest
from tests.unit_tests.monkey_island.conftest import init_mock_security_app

from monkey_island.cc.services.authentication_service.authentication_facade import (
    AuthenticationFacade,
)
from monkey_island.cc.services.authentication_service.flask_resources import (
    AgentOTP,
    AgentOTPLogin,
    Login,
    Logout,
    Register,
    RegistrationStatus,
)


@pytest.fixture
def mock_authentication_facade():
    mock_service = MagicMock(spec=AuthenticationFacade)

    return mock_service


@pytest.fixture
def build_flask_client(mock_authentication_facade):
    def inner():
        return get_mock_auth_app(mock_authentication_facade).test_client()

    return inner


def get_mock_auth_app(authentication_facade: AuthenticationFacade):
    app, api = init_mock_security_app()
    api.add_resource(Register, *Register.urls, resource_class_args=(authentication_facade,))
    api.add_resource(Login, *Login.urls, resource_class_args=(authentication_facade,))
    api.add_resource(Logout, *Logout.urls, resource_class_args=(authentication_facade,))
    api.add_resource(
        RegistrationStatus, *RegistrationStatus.urls, resource_class_args=(authentication_facade,)
    )
    api.add_resource(AgentOTP, *AgentOTP.urls)
    api.add_resource(AgentOTPLogin, *AgentOTPLogin.urls)

    return app


@pytest.fixture
def flask_client(build_flask_client, mock_authentication_facade):
    with build_flask_client() as flask_client:
        yield flask_client
