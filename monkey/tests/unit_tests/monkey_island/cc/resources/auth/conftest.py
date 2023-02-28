from unittest.mock import MagicMock

import pytest
from tests.common import StubDIContainer

from monkey_island.cc.services import AuthenticationService


@pytest.fixture
def mock_authentication_service():
    mock_service = MagicMock(spec=AuthenticationService)
    mock_service.authenticate = MagicMock()
    mock_service.reset_island = MagicMock()

    return mock_service


@pytest.fixture
def flask_client(build_flask_client, mock_authentication_service):
    container = StubDIContainer()

    container.register_instance(AuthenticationService, mock_authentication_service)

    with build_flask_client(container) as flask_client:
        yield flask_client
