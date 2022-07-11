import pytest
from tests.common import StubDIContainer
from tests.monkey_island import StubPropagationCredentialsRepository

from monkey_island.cc.repository import ICredentialsRepository


@pytest.fixture
def flask_client(build_flask_client):
    container = StubDIContainer()

    container.register(ICredentialsRepository, StubPropagationCredentialsRepository)

    with build_flask_client(container) as flask_client:
        yield flask_client
