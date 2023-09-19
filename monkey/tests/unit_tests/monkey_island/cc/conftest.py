from unittest.mock import MagicMock

import pytest
from tests.common import StubDIContainer
from tests.monkey_island import OpenErrorFileRepository
from tests.unit_tests.monkey_island.cc.mongomock_fixtures import *  # noqa: F401,F403,E402
from tests.unit_tests.monkey_island.conftest import init_mock_security_app

import monkey_island.cc.app
from monkey_island.cc.repositories import IFileRepository
from monkey_island.cc.server_utils.encryption import ILockableEncryptor


def reverse(data: bytes) -> bytes:
    return bytes(reversed(data))


@pytest.fixture
def repository_encryptor():
    # NOTE: Tests will fail if any inputs to this mock encryptor are palindromes.
    repository_encryptor = MagicMock(spec=ILockableEncryptor)
    repository_encryptor.encrypt = MagicMock(side_effect=reverse)
    repository_encryptor.decrypt = MagicMock(side_effect=reverse)

    return repository_encryptor


@pytest.fixture
def flask_client():
    container = MagicMock()
    container.resolve_dependencies.return_value = []

    with get_mock_app(container).test_client() as client:
        yield client


@pytest.fixture
def build_flask_client():
    def inner(container):
        return get_mock_app(container).test_client()

    return inner


@pytest.fixture
def build_flask_client_with_resources():
    def inner(container, resources):
        return get_mock_app(container, resources).test_client()

    return inner


def get_mock_app(container, resources=[]):
    app, api = init_mock_security_app()
    flask_resource_manager = monkey_island.cc.app.FlaskDIWrapper(api, container)
    for resource in resources:
        flask_resource_manager.add_resource(resource)
    monkey_island.cc.app.init_api_resources(flask_resource_manager)

    return app


@pytest.fixture
def open_error_flask_client(build_flask_client):
    container = StubDIContainer()
    container.register(IFileRepository, OpenErrorFileRepository)

    with build_flask_client(container) as flask_client:
        yield flask_client
